const express = require('express');
const db = require('../database');
const { authenticateToken, authorizeRoles } = require('../middleware/auth');

const router = express.Router();

// Get tasks belonging ONLY to the authenticated user
router.get('/', authenticateToken, (req, res) => {
  const sql = `SELECT id, title FROM tasks WHERE user_id = ?`;
  db.all(sql, [req.user.id], (err, rows) => {
    if (err) return res.status(500).json({ error: 'Database error' });
    res.json({ tasks: rows });
  });
});

// Create a task for the authenticated user
router.post('/', authenticateToken, (req, res) => {
  const { title } = req.body;
  if (!title) return res.status(400).json({ error: 'Title required' });

  const sql = `INSERT INTO tasks (title, user_id) VALUES (?, ?)`;
  db.run(sql, [title, req.user.id], function (err) {
    if (err) return res.status(500).json({ error: 'Database error' });
    res.status(201).json({ id: this.lastID, title });
  });
});

// ADMIN ONLY: View all tasks across all users
router.get('/admin/all', authenticateToken, authorizeRoles('admin'), (req, res) => {
  const sql = `
    SELECT tasks.id, tasks.title, users.username 
    FROM tasks 
    JOIN users ON tasks.user_id = users.id
  `;
  db.all(sql, [], (err, rows) => {
    if (err) return res.status(500).json({ error: 'Database error' });
    res.json({ allTasks: rows });
  });
});

module.exports = router;
