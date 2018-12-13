# image - 素材表
db.image.ensureIndex({'kind':1}, {background: true});
db.image.ensureIndex({'created_on':-1}, {background: true});
db.image.ensureIndex({'random':1}, {background: true});
db.image.ensureIndex({'evt':1}, {background: true});
db.image.ensureIndex({'channel':1}, {background: true});
db.image.ensureIndex({'img_url':1}, {background: true});
db.image.ensureIndex({'total_tags':1}, {background: true});
db.image.ensureIndex({'prize_id':1}, {background: true});
db.image.ensureIndex({'brand_id':1}, {background: true});
db.image.ensureIndex({'category_id':1}, {background: true});
db.image.ensureIndex({'stick_on':-1}, {background: true});
db.image.ensureIndex({'title':1}, {background: true});
