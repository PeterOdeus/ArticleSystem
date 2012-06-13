package org.peter.web.w.controller;

import java.io.IOException;

import javax.servlet.ServletException;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

import com.volvo.vplf.spring.helper.SpringHelper;

@Controller
@RequestMapping("")
public class StartController {

	/**
	 * A method that answers to the /start URL under the Spring MVC managed URL span.
	 * @return  A ModelAndView which SpringMVC passes to the viewResolver bean to resolve
	 * the view for the given viewName ("start") and renders that view using the data 
	 * in the model.
	 */
    @RequestMapping(value="/start", method = RequestMethod.GET)
    public ModelAndView handleStart() throws ServletException, IOException {
		// Create a ModelAndView with viewName "start"
		ModelAndView mav = new ModelAndView("start");
		// Add a "name" attribute to the model
		mav.addObject("name", "VPLF");
		return mav;
    }
	
}
