db.auth("root","usrtcc")

db = db.getSiblingDB("tcc")

db.createUser(
    {
        user:"usrtcc",
        pwd:"usrtcc",
        roles:[
            {
                role:"readWrite",
                db:"tcc"
            }
        ]
    }
)
