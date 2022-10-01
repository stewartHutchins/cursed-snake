#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include "./netty.h"

struct CurlResponse {
    char *ptr;
    size_t len;
};

static size_t write_callback(char *ptr_in,
                             size_t size,
                             size_t nmemb,
                             void *userdata)
{
    struct CurlResponse *response = (struct CurlResponse *) userdata;
    if (response->ptr == NULL) {
        response->ptr = (char *) malloc((size * nmemb) + 1);
        if (response->ptr == NULL) {
            return 0;
        }

        response->ptr[size * nmemb] = '\0';
        response->len = size * nmemb;
        memcpy(response->ptr, ptr_in, size * nmemb);
    } else {
        // We have to sellotape the chunks together
        response->ptr = (char *) realloc(response->ptr,
                                         response->len + (size * nmemb) + 1);
        if (response->ptr == NULL) {
            return 0;
        }

        response->ptr[response->len + (size * nmemb)] = '\0';
        memcpy(response->ptr + response->len, ptr_in, size * nmemb);
        response->len += size * nmemb;
    }

    return size * nmemb;
}

static void freeCurlResponse(struct CurlResponse *resp)
{
    if (resp->ptr) {
        free(resp->ptr);
        resp->ptr = NULL;
    }
}

int transmit_movement(config_t config, movement_t movement)
{
  const char *str = movement_to_str(movement);
    CURL *curl = curl_easy_init();
    if(curl) {
        CURLcode res;

        struct CurlResponse response = {NULL, 0};

        struct curl_slist *list = NULL;
        list = curl_slist_append(list, "Accept: application/json");
        list = curl_slist_append(list, "Content-Type: application/json");

        // Set timeouts
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 2L);

        // Set url, user-agent and, headers
        curl_easy_setopt(curl, CURLOPT_URL, config.connection_string);
        curl_easy_setopt(curl, CURLOPT_USE_SSL, 1L);
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "curl");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
        curl_easy_setopt(curl, CURLOPT_HTTPPOST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, str);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, strlen(str));
        curl_easy_setopt(curl, CURLOPT_POST, 1L);

        // Set response write
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *) &response);

        res = curl_easy_perform(curl);

        int getSuccess = res == CURLE_OK && response.ptr != NULL;
        curl_easy_cleanup(curl);
        curl_slist_free_all(list);
     
        freeCurlResponse(&response);

        if (!getSuccess) {
          return 0;
        }

        return 1;
    } else {
        return 0;
    }
}
