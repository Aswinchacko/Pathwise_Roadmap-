const express = require('express')
const jwt = require('jsonwebtoken')
const { OAuth2Client } = require('google-auth-library')
const axios = require('axios')
const User = require('../models/User')
const auth = require('../middleware/auth')

const router = express.Router()
const googleClient = new OAuth2Client(process.env.GOOGLE_CLIENT_ID)

// Register
router.post('/register', async (req, res) => {
  try {
    const { firstName, lastName, email, password } = req.body

    // Check if user already exists
    const existingUser = await User.findOne({ email })
    if (existingUser) {
      return res.status(400).json({ message: 'User already exists with this email' })
    }

    // Create new user
    const user = new User({
      firstName,
      lastName,
      email,
      password
    })

    await user.save()

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE || '24h' }
    )

    res.status(201).json({
      message: 'User registered successfully',
      token,
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true
      }
    })
  } catch (error) {
    console.error('Register error:', error)
    res.status(500).json({ message: 'Server error' })
  }
})

// Login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body

    // Find user by email
    const user = await User.findOne({ email })
    if (!user) {
      return res.status(400).json({ message: 'Invalid credentials' })
    }

    // Check password
    const isPasswordValid = await user.comparePassword(password)
    if (!isPasswordValid) {
      return res.status(400).json({ message: 'Invalid credentials' })
    }

    // Update last login
    user.lastLogin = new Date()
    await user.save()

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE || '24h' }
    )

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true
      }
    })
  } catch (error) {
    console.error('Login error:', error)
    res.status(500).json({ message: 'Server error' })
  }
})

// Google OAuth
router.post('/google', async (req, res) => {
  try {
    const { token } = req.body

    if (!token) {
      return res.status(400).json({ message: 'Google token is required' })
    }

    // Check if Google OAuth is configured
    if (!process.env.GOOGLE_CLIENT_ID || process.env.GOOGLE_CLIENT_ID === 'your_google_client_id_here') {
      return res.status(500).json({ message: 'Google OAuth is not configured' })
    }

    // Verify Google token
    const ticket = await googleClient.verifyIdToken({
      idToken: token,
      audience: process.env.GOOGLE_CLIENT_ID
    })

    const payload = ticket.getPayload()
    const { sub: googleId, email, given_name: firstName, family_name: lastName } = payload

    // Handle missing names from Google
    const userFirstName = firstName || 'User'
    const userLastName = lastName || ''

    // Check if user exists
    let user = await User.findOne({ 
      $or: [
        { googleId },
        { email }
      ]
    })

    if (!user) {
      // Create new user
      user = new User({
        firstName: userFirstName,
        lastName: userLastName,
        email,
        googleId,
        googleEmail: email
      })
    } else {
      // Update existing user with Google info if needed
      if (!user.googleId) {
        user.googleId = googleId
        user.googleEmail = email
        // Update names if they're missing
        if (!user.firstName && userFirstName) {
          user.firstName = userFirstName
        }
        if (!user.lastName && userLastName) {
          user.lastName = userLastName
        }
      }
    }

    // Update last login
    user.lastLogin = new Date()
    await user.save()

    // Generate JWT token
    const jwtToken = jwt.sign(
      { userId: user._id },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE || '24h' }
    )

    res.json({
      message: 'Google login successful',
      token: jwtToken,
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true
      }
    })
  } catch (error) {
    console.error('Google login error:', error)
    if (error.message.includes('Wrong recipient')) {
      return res.status(400).json({ message: 'Invalid Google token or OAuth not configured properly' })
    }
    res.status(500).json({ message: 'Server error' })
  }
})

// GitHub OAuth
router.post('/github', async (req, res) => {
  try {
    const { code } = req.body

    if (!code) {
      return res.status(400).json({ message: 'GitHub authorization code is required' })
    }

    // Check if GitHub OAuth is configured
    if (!process.env.GITHUB_CLIENT_ID || !process.env.GITHUB_CLIENT_SECRET || 
        process.env.GITHUB_CLIENT_ID === 'your_github_client_id_here' || 
        process.env.GITHUB_CLIENT_SECRET === 'your_github_client_secret_here') {
      return res.status(500).json({ message: 'GitHub OAuth is not configured' })
    }

    // Exchange code for access token
    const tokenResponse = await axios.post('https://github.com/login/oauth/access_token', {
      client_id: process.env.GITHUB_CLIENT_ID,
      client_secret: process.env.GITHUB_CLIENT_SECRET,
      code: code
    }, {
      headers: {
        'Accept': 'application/json'
      }
    })

    const { access_token } = tokenResponse.data

    if (!access_token) {
      return res.status(400).json({ message: 'Failed to get GitHub access token' })
    }

    // Get user data from GitHub
    const userResponse = await axios.get('https://api.github.com/user', {
      headers: {
        'Authorization': `token ${access_token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    })

    const githubUser = userResponse.data
    const { id: githubId, login: githubUsername, name, email } = githubUser

    // Get user's email if not provided
    let userEmail = email
    if (!userEmail) {
      const emailsResponse = await axios.get('https://api.github.com/user/emails', {
        headers: {
          'Authorization': `token ${access_token}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      })
      const primaryEmail = emailsResponse.data.find(email => email.primary)
      userEmail = primaryEmail ? primaryEmail.email : null
    }

    if (!userEmail) {
      return res.status(400).json({ message: 'GitHub email is required' })
    }

    // Parse name into firstName and lastName
    let firstName = 'User'
    let lastName = ''
    if (name) {
      const nameParts = name.split(' ')
      firstName = nameParts[0] || 'User'
      lastName = nameParts.slice(1).join(' ') || ''
    }

    // Check if user exists
    let user = await User.findOne({ 
      $or: [
        { githubId },
        { email: userEmail }
      ]
    })

    if (!user) {
      // Create new user
      user = new User({
        firstName,
        lastName,
        email: userEmail,
        githubId: githubId.toString(),
        githubUsername
      })
    } else {
      // Update existing user with GitHub info if needed
      if (!user.githubId) {
        user.githubId = githubId.toString()
        user.githubUsername = githubUsername
        // Update names if they're missing
        if (!user.firstName && firstName) {
          user.firstName = firstName
        }
        if (!user.lastName && lastName) {
          user.lastName = lastName
        }
      }
    }

    // Update last login
    user.lastLogin = new Date()
    await user.save()

    // Generate JWT token
    const jwtToken = jwt.sign(
      { userId: user._id },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE || '24h' }
    )

    res.json({
      message: 'GitHub login successful',
      token: jwtToken,
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true
      }
    })
  } catch (error) {
    console.error('GitHub login error:', error)
    if (error.response && error.response.status === 404) {
      return res.status(400).json({ message: 'Invalid GitHub authorization code or OAuth not configured properly' })
    }
    res.status(500).json({ message: 'Server error' })
  }
})

// LinkedIn OAuth
router.post('/linkedin', async (req, res) => {
  try {
    const { code } = req.body

    if (!code) {
      return res.status(400).json({ message: 'LinkedIn authorization code is required' })
    }

    // Exchange code for access token
    const tokenResponse = await axios.post('https://www.linkedin.com/oauth/v2/accessToken', {
      grant_type: 'authorization_code',
      client_id: process.env.LINKEDIN_CLIENT_ID,
      client_secret: process.env.LINKEDIN_CLIENT_SECRET,
      code: code,
      redirect_uri: process.env.LINKEDIN_REDIRECT_URI
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    const { access_token } = tokenResponse.data

    if (!access_token) {
      return res.status(400).json({ message: 'Failed to get LinkedIn access token' })
    }

    // Get user data from LinkedIn
    const userResponse = await axios.get('https://api.linkedin.com/v2/me', {
      headers: {
        'Authorization': `Bearer ${access_token}`,
        'X-Restli-Protocol-Version': '2.0.0'
      }
    })

    const linkedinUser = userResponse.data
    const { id: linkedinId, localizedFirstName: firstName, localizedLastName: lastName } = linkedinUser

    // Get user's email from LinkedIn
    const emailResponse = await axios.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))', {
      headers: {
        'Authorization': `Bearer ${access_token}`,
        'X-Restli-Protocol-Version': '2.0.0'
      }
    })

    const emailElement = emailResponse.data.elements?.[0]
    const userEmail = emailElement?.['handle~']?.emailAddress

    if (!userEmail) {
      return res.status(400).json({ message: 'LinkedIn email is required' })
    }

    // Handle missing names from LinkedIn
    const userFirstName = firstName || 'User'
    const userLastName = lastName || ''

    // Check if user exists
    let user = await User.findOne({ 
      $or: [
        { linkedinId },
        { email: userEmail }
      ]
    })

    if (!user) {
      // Create new user
      user = new User({
        firstName: userFirstName,
        lastName: userLastName,
        email: userEmail,
        linkedinId: linkedinId.toString(),
        linkedinEmail: userEmail
      })
    } else {
      // Update existing user with LinkedIn info if needed
      if (!user.linkedinId) {
        user.linkedinId = linkedinId.toString()
        user.linkedinEmail = userEmail
        // Update names if they're missing
        if (!user.firstName && userFirstName) {
          user.firstName = userFirstName
        }
        if (!user.lastName && userLastName) {
          user.lastName = userLastName
        }
      }
    }

    // Update last login
    user.lastLogin = new Date()
    await user.save()

    // Generate JWT token
    const jwtToken = jwt.sign(
      { userId: user._id },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE || '24h' }
    )

    res.json({
      message: 'LinkedIn login successful',
      token: jwtToken,
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true
      }
    })
  } catch (error) {
    console.error('LinkedIn login error:', error)
    res.status(500).json({ message: 'Server error' })
  }
})

// Get user profile (protected route)
router.get('/profile', auth, async (req, res) => {
  try {
    const user = req.user
    res.json({
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true,
        lastLogin: user.lastLogin,
        createdAt: user.createdAt,
        // Extended profile fields
        full_name: user.full_name,
        phone: user.phone,
        location: user.location,
        summary: user.summary,
        skills: user.skills || [],
        education: user.education || [],
        experience: user.experience || [],
        projects: user.projects || [],
        certifications: user.certifications || [],
        languages: user.languages || [],
        preferences: user.preferences || {
          emailNotifications: true,
          weeklyReports: false,
          theme: 'auto'
        }
      }
    })
  } catch (error) {
    console.error('Profile error:', error)
    res.status(500).json({ message: 'Server error' })
  }
})

// Update user profile (protected route)
router.put('/profile', auth, async (req, res) => {
  try {
    const {
      firstName,
      lastName,
      full_name,
      phone,
      location,
      summary,
      skills,
      education,
      experience,
      projects,
      certifications,
      languages,
      preferences
    } = req.body

    const user = await User.findById(req.user._id)
    
    // Update basic fields
    if (firstName !== undefined) user.firstName = firstName
    if (lastName !== undefined) user.lastName = lastName
    
    // Update extended profile fields
    if (full_name !== undefined) user.full_name = full_name
    if (phone !== undefined) user.phone = phone
    if (location !== undefined) user.location = location
    if (summary !== undefined) user.summary = summary
    if (skills !== undefined) user.skills = skills
    if (education !== undefined) user.education = education
    if (experience !== undefined) user.experience = experience
    if (projects !== undefined) user.projects = projects
    if (certifications !== undefined) user.certifications = certifications
    if (languages !== undefined) user.languages = languages
    
    // Update preferences
    if (preferences !== undefined) {
      user.preferences = { ...user.preferences, ...preferences }
    }

    await user.save()

    res.json({
      message: 'Profile updated successfully',
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true,
        full_name: user.full_name,
        phone: user.phone,
        location: user.location,
        summary: user.summary,
        skills: user.skills || [],
        education: user.education || [],
        experience: user.experience || [],
        projects: user.projects || [],
        certifications: user.certifications || [],
        languages: user.languages || [],
        preferences: user.preferences
      }
    })
  } catch (error) {
    console.error('Update profile error:', error)
    res.status(500).json({ message: 'Server error' })
  }
})

// Update profile from resume data (protected route)
router.put('/profile/from-resume', auth, async (req, res) => {
  try {
    const resumeData = req.body
    const user = await User.findById(req.user._id)
    
    // Map resume data to user profile fields
    if (resumeData.name) {
      const nameParts = resumeData.name.split(' ')
      user.firstName = nameParts[0] || user.firstName
      user.lastName = nameParts.slice(1).join(' ') || user.lastName
      user.full_name = resumeData.name
    }
    
    if (resumeData.email && !user.email) user.email = resumeData.email
    if (resumeData.phone) user.phone = resumeData.phone
    if (resumeData.location) user.location = resumeData.location
    if (resumeData.summary) user.summary = resumeData.summary
    
    // Merge skills (avoid duplicates)
    if (resumeData.skills && Array.isArray(resumeData.skills)) {
      const existingSkills = user.skills || []
      const newSkills = resumeData.skills.filter(skill => 
        !existingSkills.some(existing => 
          existing.toLowerCase() === skill.toLowerCase()
        )
      )
      user.skills = [...existingSkills, ...newSkills]
    }
    
    // Update education
    if (resumeData.education && Array.isArray(resumeData.education)) {
      user.education = resumeData.education.map(edu => ({
        degree: edu.degree || edu.title,
        institution: edu.institution || edu.school,
        year_start: edu.year_start || edu.start_year,
        year_end: edu.year_end || edu.end_year,
        dates: edu.dates,
        gpa: edu.gpa
      }))
    }
    
    // Update experience
    if (resumeData.experience && Array.isArray(resumeData.experience)) {
      user.experience = resumeData.experience.map(exp => ({
        role: exp.role || exp.title || exp.position,
        title: exp.title || exp.role || exp.position,
        company: exp.company || exp.employer,
        year_start: exp.year_start || exp.start_year,
        year_end: exp.year_end || exp.end_year,
        dates: exp.dates,
        description: exp.description || exp.responsibilities
      }))
    }
    
    // Update projects
    if (resumeData.projects && Array.isArray(resumeData.projects)) {
      user.projects = resumeData.projects.map(project => ({
        title: project.title || project.name,
        description: project.description,
        technologies: project.technologies || project.tech_stack || [],
        url: project.url || project.link
      }))
    }
    
    // Update certifications
    if (resumeData.certifications && Array.isArray(resumeData.certifications)) {
      user.certifications = resumeData.certifications
    }
    
    // Update languages
    if (resumeData.languages && Array.isArray(resumeData.languages)) {
      user.languages = resumeData.languages
    }

    await user.save()

    res.json({
      message: 'Profile updated from resume successfully',
      user: {
        id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        isAdmin: user.isAdmin === 'true' || user.isAdmin === true,
        full_name: user.full_name,
        phone: user.phone,
        location: user.location,
        summary: user.summary,
        skills: user.skills || [],
        education: user.education || [],
        experience: user.experience || [],
        projects: user.projects || [],
        certifications: user.certifications || [],
        languages: user.languages || [],
        preferences: user.preferences
      }
    })
  } catch (error) {
    console.error('Update profile from resume error:', error)
    res.status(500).json({ message: 'Server error' })
  }
})

module.exports = router 