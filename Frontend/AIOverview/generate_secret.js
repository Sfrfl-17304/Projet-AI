import crypto from 'crypto';
const secret = crypto.randomBytes(64).toString('hex');
console.log('Generated SESSION_SECRET:');
console.log(secret);
