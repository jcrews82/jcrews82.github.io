const fs = require('fs');
const path = require('path');

const VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif'];
const VALID_CATEGORIES = ['pedals', 'guitars', 'amps'];

exports.handler = async function(event) {
  const category = event.queryStringParameters && event.queryStringParameters.category;

  if (!category || !VALID_CATEGORIES.includes(category)) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Invalid or missing category. Use: pedals, guitars, amps' })
    };
  }

  try {
    // In Netlify, the site root is at /var/task
    const folderPath = path.join('/var/task', 'images', category);

    if (!fs.existsSync(folderPath)) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify([])
      };
    }

    const files = fs.readdirSync(folderPath)
      .filter(f => VALID_EXTENSIONS.includes(path.extname(f).toLowerCase()))
      .sort();

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify(files)
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};
