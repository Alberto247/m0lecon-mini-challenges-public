db.createUser({
  user: 'th3pwn3r',
  pwd: 'W2Zyr&Np',
  roles: [
    {
      role: 'read',
      db: 'test',
    },
  ],
});

db.createCollection('posts', {capped: false});
db.posts.insert([
	{"content": "ptm{Y0u_h4ve_s0m3_w1z4rds_eyes!}", visible: false},
	{"content": "You man you cool post", visible: true},
	{"content": "Very interesting post, thanks for sharing it.", visible: true},
	{"content": "This is garbage mate, just remove it.", visible: true},
]);
