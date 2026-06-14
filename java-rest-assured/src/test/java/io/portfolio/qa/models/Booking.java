package io.portfolio.qa.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Booking POJO for restful-booker.
 *
 * Lombok generates the boilerplate; Jackson handles (de)serialization. We ignore
 * unknown properties so the suite doesn't break the day booker adds a field, and
 * we drop nulls on the way out so a PATCH body only carries what we set.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Booking {

    private String firstname;
    private String lastname;
    private Integer totalprice;
    private Boolean depositpaid;
    private BookingDates bookingdates;
    private String additionalneeds;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class BookingDates {
        // booker exchanges these as plain ISO date strings; keeping them String
        // avoids a timezone round-tripping headache for no real gain here.
        private String checkin;
        private String checkout;
    }
}
