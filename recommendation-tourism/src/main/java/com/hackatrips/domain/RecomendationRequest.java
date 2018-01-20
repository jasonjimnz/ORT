package com.hackatrips.domain;

import lombok.Data;

@Data
public class RecomendationRequest {
    private String destination;

    private String origin;
}
