package com.badjin.test1_login

import javax.persistence.Entity
import javax.persistence.GeneratedValue
import javax.persistence.Id

@Entity
data class UserData (
        var userID: String,
        var password: String,
        @Id @GeneratedValue var id : Long? = null
)