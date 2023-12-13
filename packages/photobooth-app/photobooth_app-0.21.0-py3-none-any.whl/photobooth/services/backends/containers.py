import logging

from dependency_injector import containers, providers
from pymitter import EventEmitter

from ...appconfig import AppConfig
from .abstractbackend import AbstractBackend
from .simulated import SimulatedBackend
from .webcamcv2 import WebcamCv2Backend

logger = logging.getLogger(__name__)


def init_res_obj_backend(_obj_: AbstractBackend, evtbus: EventEmitter, config: AppConfig):
    """actually same as in parent container."""
    _backend = None

    try:
        _backend = _obj_(evtbus, config)
        _backend.start()
    except Exception as exc:
        logger.exception(exc)
        logger.critical("could not init/start backend")

    finally:
        yield _backend

    try:
        if _backend:  # if not none
            _backend.stop()
    except Exception as exc:
        logger.exception(exc)
        logger.critical("could not stop backend")


class BackendsContainer(containers.DeclarativeContainer):
    evtbus = providers.Dependency(instance_of=EventEmitter)
    config = providers.Dependency(instance_of=AppConfig)

    ## Services: Backends (for image aquisition)
    disabled_backend = providers.Object(None)
    simulated_backend = providers.Resource(init_res_obj_backend, SimulatedBackend, evtbus, config)
    webcamcv2_backend = providers.Resource(init_res_obj_backend, WebcamCv2Backend, evtbus, config)
    picamera2_backend = providers.Object(None)
    gphoto2_backend = providers.Object(None)
    webcamv4l_backend = providers.Object(None)

    # picamera2 backend import
    try:
        from .picamera2_ import Picamera2Backend

        picamera2_backend = providers.Resource(init_res_obj_backend, Picamera2Backend, evtbus, config)
        print("added provider for picamera2 backend")
    except Exception:
        # logger is not avail at this point yet, so print:
        print("skipped import picamera2 backend")

    # gphoto2 backend import
    try:
        from .gphoto2 import Gphoto2Backend

        gphoto2_backend = providers.Resource(init_res_obj_backend, Gphoto2Backend, evtbus, config)
        print("added provider for gphoto2 backend")
    except Exception:
        # logger is not avail at this point yet, so print:
        print("skipped import gphoto2 backend")

    # gphoto2 backend import
    try:
        from .webcamv4l import WebcamV4lBackend

        webcamv4l_backend = providers.Resource(init_res_obj_backend, WebcamV4lBackend, evtbus, config)
        print("added provider for webcamv4l backend")
    except Exception:
        # logger is not avail at this point yet, so print:
        print("skipped import webcamv4l backend")

    # following are to be used in aquisitionservice

    backends_set = {
        "disabled": disabled_backend,
        "simulated": simulated_backend,
        "webcamcv2": webcamcv2_backend,
        "picamera2": picamera2_backend,
        "gphoto2": gphoto2_backend,
        "webcamv4l": webcamv4l_backend,
    }

    primary_backend = providers.Selector(
        providers.Callable(lambda cfg_enum: cfg_enum.backends.MAIN_BACKEND.lower(), cfg_enum=config),
        **backends_set,
    )

    secondary_backend = providers.Selector(
        providers.Callable(lambda cfg_enum: cfg_enum.backends.LIVE_BACKEND.lower(), cfg_enum=config),
        **backends_set,
    )
