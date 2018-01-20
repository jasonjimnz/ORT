package com.hackatrips.boot;

import com.hackatrips.domain.Destination;
import com.hackatrips.domain.RecomendationResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.ArrayList;
import java.util.List;

@Controller
public class WebNeo4jController {

    // dummy para integrate bootstrap to spring boot
    @RequestMapping(value="/",method = RequestMethod.GET)
    public String home(){
        return "dummy";
    }

    // ejemplo para llamar al interfaz rest
    @RequestMapping(value="/web",method = RequestMethod.GET)
    public String destinations(){
        return "index";
    }

    // ejemplo que devuelve los destinations
    @ResponseBody
    @RequestMapping(value="/web/destinations1",method = RequestMethod.GET)
    public String testGreetig() {
        return "Message From oracle cloud web servicce  - Hello World!";
    }

    @RequestMapping(path = "/web/destinations", method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<RecomendationResponse> obtainDestinations(
            @RequestParam(value="origin", defaultValue="Barccelona") String origin,
            @RequestParam(value="destination", defaultValue="Madrid") String destination
    ) {
        RecomendationResponse response = new RecomendationResponse();

        Destination destination1 = new Destination("destinatio1", 2.3F);
        Destination destination2 = new Destination("destinatio2", 4.3F);
        Destination destination3 = new Destination("destinatio3", 6.3F);
        List<Destination> destinations = new ArrayList<>();

        // call template rest
        destinations.add(destination1);
        destinations.add(destination2);
        destinations.add(destination3);
        response.setDestinations(destinations);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}
