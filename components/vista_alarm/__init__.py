import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    STATE_CLASS_MEASUREMENT,
    UNIT_DEGREES,
    UNIT_KILOMETER_PER_HOUR,
    UNIT_METER,
)
from esphome.components import time, api, text_sensor
# from esphome.esphome.cpp_generator import ParameterListExpression


CONF_RXPIN="rxPin"
CONF_TXPIN="txPin"
CONF_MONITORPIN="monitorPin"
CONF_ACCESSCODE="accessCode"
CONF_QUICKARM="quickArm"
CONF_EXPANDER_ADDR_1="expanderAddr1"
CONF_EXPANDER_ADDR_2="expanderAddr2"
CONF_RELAY_ADDR_1="relayAddr1"
CONF_RELAY_ADDR_2="relayAddr2"
CONF_RELAY_ADDR_3="relayAddr3"
CONF_RELAY_ADDR_4="relayAddr4"
CONF_TTL="TTL"
CONF_LRR_SUPERVISOR="lrrSupervisor"
CONF_DEBUG="debug"
CONF_DEFAULT_PARTITION="defaultPartition"

CONF_PARTITION_1 = "partition1"
CONF_PARTITION_2 = "partition2"
CONF_PARTITION_3 = "partition3"
CONF_KEYPAD_ADDR="keypadAddr"
CONF_SYSTEM_STATUS="systemStatus"
CONF_LINE1_DISPLAY="line1Display"
CONF_LINE2_DISPLAY="line2Display"
CONF_BEEPS="beeps"


DEPENDENCIES = ["api", "globals", "time"]
AUTO_LOAD = ["sensor", "text_sensor"]

VISTAECPHOME = cg.esphome_ns.class_("vistaECPHome", cg.Component, time.RealTimeClock)


MULTI_CONF = True
CONFIG_SCHEMA_PER_PARTITION = cv.All(
    cv.Schema(
        {
            cv.Required(CONF_KEYPAD_ADDR): int,
            cv.Optional(CONF_SYSTEM_STATUS): text_sensor.TEXT_SENSOR_SCHEMA,
            cv.Optional(CONF_LINE1_DISPLAY): text_sensor.TEXT_SENSOR_SCHEMA,
            cv.Optional(CONF_LINE2_DISPLAY): text_sensor.TEXT_SENSOR_SCHEMA,
            cv.Optional(CONF_BEEPS): text_sensor.TEXT_SENSOR_SCHEMA,
        }
    )
)


CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(VISTAECPHOME),
            cv.Required(CONF_RXPIN): int,
            cv.Required(CONF_TXPIN): int,
            cv.Required(CONF_MONITORPIN): int,
            cv.Required(CONF_ACCESSCODE): str,
            cv.Required(CONF_QUICKARM): bool,
            cv.Required(CONF_EXPANDER_ADDR_1): int,
            cv.Required(CONF_EXPANDER_ADDR_2): int,
            cv.Required(CONF_RELAY_ADDR_1): int,
            cv.Required(CONF_RELAY_ADDR_2): int,
            cv.Required(CONF_RELAY_ADDR_3): int,
            cv.Required(CONF_RELAY_ADDR_4): int,
            cv.Required(CONF_TTL): int,
            cv.Required(CONF_LRR_SUPERVISOR): bool,
            cv.Required(CONF_DEBUG): int,
            cv.Optional(CONF_DEFAULT_PARTITION, default=CONF_PARTITION_1): str,
            cv.Optional(CONF_PARTITION_1): CONFIG_SCHEMA_PER_PARTITION,
            cv.Optional(CONF_PARTITION_2): CONFIG_SCHEMA_PER_PARTITION,
            cv.Optional(CONF_PARTITION_3): CONFIG_SCHEMA_PER_PARTITION,
        }
    )
)

async def to_code_per_partition(var, partition: int, config_partition):
    keypadAddr = config_partition[CONF_KEYPAD_ADDR]

    # for conf_text_sensor in [CONF_SYSTEM_STATUS]

    if CONF_SYSTEM_STATUS in config_partition:
        system_status = await text_sensor.new_text_sensor(config_partition[CONF_SYSTEM_STATUS])
    else:
        system_status = None

    if CONF_LINE1_DISPLAY in config_partition:
        line1_display = await text_sensor.new_text_sensor(config_partition[CONF_LINE1_DISPLAY])
    else:
        line1_display = None

    if CONF_LINE2_DISPLAY in config_partition:
        line2_display = await text_sensor.new_text_sensor(config_partition[CONF_LINE2_DISPLAY])
    else:
        line2_display = None

    if CONF_BEEPS in config_partition:
        beeps = await text_sensor.new_text_sensor(config_partition[CONF_BEEPS])
    else:
        beeps = None

    cg.add(var.setPartition(partition, keypadAddr, system_status, line1_display, line2_display, beeps))


async def to_code(config):
    default_partition=config[CONF_DEFAULT_PARTITION]
    keypadAddr1 = config[default_partition][CONF_KEYPAD_ADDR]
    txPin = config[CONF_TXPIN]
    rxPin = config[CONF_RXPIN]
    monitorPin = config[CONF_MONITORPIN]

    var = cg.new_Pvariable(config[CONF_ID], keypadAddr1, rxPin, txPin, monitorPin)
    await cg.register_component(var, config)

    if CONF_PARTITION_1 in config:
        await to_code_per_partition(var, 1, config[CONF_PARTITION_1])

    # if CONF_PARTITION_2 in config:
    #     to_code_partition(var, 2, config[CONF_PARTITION_2])

    # if CONF_PARTITION_3 in config:
    #     to_code_partition(var, 3, config[CONF_PARTITION_3])


    # if CONF_PARTITION_1 in config:
    #     config_partition = config[CONF_PARTITION_1]
    #     keypadAddr = config_partition[CONF_KEYPAD_ADDR]

    #     if CONF_SYSTEM_STATUS in config_partition:
    #         system_status = await text_sensor.new_text_sensor(config_partition[CONF_SYSTEM_STATUS])
    #     else:
    #         system_status = None

    #     if CONF_LINE1_DISPLAY in config_partition:
    #         line1_display = await text_sensor.new_text_sensor(config_partition[CONF_LINE1_DISPLAY])
    #     else:
    #         line1_display = None

    #     if CONF_LINE2_DISPLAY in config_partition:
    #         line2_display = await text_sensor.new_text_sensor(config_partition[CONF_LINE2_DISPLAY])
    #     else:
    #         line2_display = None

    #     if CONF_BEEPS in config_partition:
    #         beeps = await text_sensor.new_text_sensor(config_partition[CONF_BEEPS])
    #     else:
    #         beeps = None

    #     cg.add(var.setPartition(1, keypadAddr, system_status, line1_display, line2_display, beeps))

    # if CONF_LONGITUDE in config:
    #     sens = await sensor.new_sensor(config[CONF_LONGITUDE])
    #     cg.add(var.set_longitude_sensor(sens))

    # if CONF_SPEED in config:
    #     sens = await sensor.new_sensor(config[CONF_SPEED])
    #     cg.add(var.set_speed_sensor(sens))

    # if CONF_COURSE in config:
    #     sens = await sensor.new_sensor(config[CONF_COURSE])
    #     cg.add(var.set_course_sensor(sens))

    # if CONF_ALTITUDE in config:
    #     sens = await sensor.new_sensor(config[CONF_ALTITUDE])
    #     cg.add(var.set_altitude_sensor(sens))

    # if CONF_SATELLITES in config:
    #     sens = await sensor.new_sensor(config[CONF_SATELLITES])
    #     cg.add(var.set_satellites_sensor(sens))
