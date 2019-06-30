package com.badjin.test1

import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.ui.set
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable

@Controller
class HtmlController {

    @GetMapping("/")
    fun index(model:Model):String{
        model["title"] = "Home"

        return "index"
    }

    @GetMapping("/{formType}")
    fun htmlForm(model:Model, @PathVariable formType:String):String{
        var response : String=""

        if (formType.equals("sign")){
            response="sign"
        }
        else if (formType.equals("login")){
            response="login"
        }
        model["title"] = response

        return response
    }


}