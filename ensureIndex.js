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

# produce - 产品库
db.produce.ensureIndex({'kind':1}, {background: true});
db.produce.ensureIndex({'created_on':-1}, {background: true});
db.produce.ensureIndex({'random':1}, {background: true});
db.produce.ensureIndex({'evt':1}, {background: true});
db.produce.ensureIndex({'channel':1}, {background: true});
db.produce.ensureIndex({'total_tags':1}, {background: true});
db.produce.ensureIndex({'prize_ids':1}, {background: true});
db.produce.ensureIndex({'brand_id':1}, {background: true});
db.produce.ensureIndex({'category_id':1}, {background: true});
db.produce.ensureIndex({'stick_on':-1}, {background: true});
db.produce.ensureIndex({'title':1}, {background: true});
db.produce.ensureIndex({'user_id':1}, {background: true});
db.produce.ensureIndex({'editor_id':1}, {background: true});
db.produce.ensureIndex({'editor_level':1}, {background: true});


# color - 色值表
db.color.ensureIndex({'rgb':1}, {background: true});
db.color.ensureIndex({'hex':1}, {background: true});
