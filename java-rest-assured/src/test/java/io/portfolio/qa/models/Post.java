package io.portfolio.qa.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * jsonplaceholder post — the body we serialize on create/update and the object
 * we deserialize back. NON_NULL keeps a PATCH body lean (only the fields we set
 * are sent), which is what lets the partial-update test assert that the server
 * left the rest untouched.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Post {

    private Integer userId;
    private Integer id;
    private String title;
    private String body;
}
