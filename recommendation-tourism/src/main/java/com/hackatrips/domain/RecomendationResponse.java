package com.hackatrips.domain;

import java.util.List;


public class RecomendationResponse {

    private List<Destination> destinations;

    public List<Destination> getDestinations() {
        return destinations;
    }

    public void setDestinations(List<Destination> destinations) {
        this.destinations = destinations;
    }
}
