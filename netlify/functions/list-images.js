const fs = require('fs');
const path = require('path');

const VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif'];
const VALID_CATEGORIES = ['pedals', 'guitars', 'amps'];

exports.handler = async function(event) {
  const category = event.queryStringParameters && event.queryStringParameters.category;

  if (!category || !VALID_CATEGORIES.includes(category)) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Invalid or missing category' })
    };
  }

  // Try multiple possible paths Netlify might use
  const possiblePaths = [
    path.join('/var/task', 'images', category),
    path.join(process.cwd(), 'images', category),
    path.join(__dirname, '..', '..', 'images', category),
    path.join(__dirname, '../../images', category),
  ];

  let files = [];
  let usedPath = null;

  for (const folderPath of possiblePaths) {
    try {
      if (fs.existsSync(folderPath)) {
        files = fs.readdirSync(folderPath)
          .filter(f => VALID_EXTENSIONS.includes(path.extname(f).toLowerCase()))
          .sort();
        usedPath = folderPath;
        break;
      }
    } catch(e) {
      continue;
    }
  }

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    body: JSON.stringify(files)
  };
};
