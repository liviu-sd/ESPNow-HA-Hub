#ifndef espnow_helpers__hpp
#define espnow_helpers__hpp

using namespace std;

#ifndef ARDUINOJSON_ENABLE_STD_STRING
    #define ARDUINOJSON_ENABLE_STD_STRING 1  // NOLINT
#endif
#ifndef ARDUINOJSON_USE_LONG_LONG
    #define ARDUINOJSON_USE_LONG_LONG 1  // NOLINT
#endif

#include <ArduinoJson.h>
// #include "ArduinoJson.h"

#include "CayenneLPP.h"

namespace ESPNowHelpers
{
    uint8_t parseJSON_O(const uint8_t* incoming_data, uint8_t data_length, JsonObject &out){
        CayenneLPP lpp(160);
        lpp.reset();

        return lpp.decodeTTN((uint8_t*)incoming_data, data_length, out);
    }
    
    size_t parseJSON_S(const uint8_t* incoming_data, uint8_t data_length, string &out){
        JsonDocument jsonBuffer;
        JsonObject root = jsonBuffer.to<JsonObject>();

        uint8_t parse_state = ESPNowHelpers::parseJSON_O(incoming_data, data_length, root);

        size_t size = 0;
        if (parse_state > 0){
            size = serializeJson(root, out);
        }

        ESP_LOGD("ESPNowHelpers", "::parseJSON_S(...) parse_state: %u, size: %u, json_data: %s", parse_state, size, out.c_str());

        return size;
    }

//    void log_message(ESPNowRecvInfo info, uint8_t *data, double size, string level = "D", string tag = "", string prefix = "") {
//    }
}

#endif //espnow_helpers__hpp
