package io.portfolio.qa.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * jsonplaceholder user. The @JsonProperty on userName shows Jackson bridging a
 * JSON key ("username") to a differently-named Java field — the kind of mapping
 * that trips people up when the wire format and the model drift apart. The
 * nested Company also exercises object-graph deserialization, not just flat
 * fields.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class User {

    private Integer id;
    private String name;

    @JsonProperty("username")
    private String userName;

    private String email;
    private String phone;
    private String website;
    private Company company;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Company {
        private String name;
        private String catchPhrase;
    }
}
