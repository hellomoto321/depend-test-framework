from utils import enter_depend_test, STEPS, RESULT, SETUP
enter_depend_test()

from depend_test_framework.core import Action, ParamsRequire, Provider, Consumer, CheckPoint, TestObject, Mist, MistDeadEndException, MistClearException


def set_ivshmem_device(params, env):
    """
    Add the ivshmem device in guest xml
    """
    if params.ivshmem.model != 'ivshmem-plain':
        raise NotImplementedError
    params.doc_logger.info(STEPS + """
    <shmem name='%s'>
      <model type='%s'/>
      <size unit='KiB'>%d</size>
    </shmem>
        """ % (params.ivshmem.name,
               params.ivshmem.model,
               params.ivshmem.size if params.ivshmem.size else 4096))

def check_ivshmem_cmdline(params, env):
    """
    check qemu command line:

    """
    params.doc_logger.info(STEPS + "# ps aux|grep %s" % params.guest_name)
    params.doc_logger.info(RESULT + """
...
-object memory-backend-file,id=shmmem-shmem0,mem-path=/dev/shm/%s,size=%d,share=yes -device ivshmem-plain,id=shmem0,memdev=shmmem-shmem0
...
""" % (params.ivshmem.name, params.ivshmem.size if params.ivshmem.size else 4194304))

def check_ivshmem_in_guest(params, env):
    """
    TODO
    """
    params.doc_logger.info(STEPS + "TODO")
    params.doc_logger.info(RESULT + "TODO")

def check_ivshmem_audit(params, env):
    """
    Check the ivshmem device audit
    """
    params.doc_logger.info(STEPS + "Make sure the auditd is running")

    start = [Provider('$guest_name.active', Provider.SET),
             Provider('$guest_name.ivshmem', Provider.CLEAR)]
    end = [Provider('$guest_name.active', Provider.SET),
             Provider('$guest_name.ivshmem', Provider.SET)]

    def check_audit_log(func, params, env):
        """
        Check the audit log
        """
        func(params, env)
        params.doc_logger.info(STEPS + "# ausearch -m VIRT_RESOURCE -ts recent")
        params.doc_logger.info(RESULT + """
...
type=VIRT_RESOURCE ... msg='virt=kvm resrc=shmem reason=attach vm="%s" uuid=c156ca6f-3c16-435b-980d-9745e1d84ad1 size=%d path=/dev/shm/%s exe="/usr/sbin/libvirtd" hostname=? addr=? terminal=? res=success'
...
        """ % (params.guest_name,
               params.ivshmem.size if params.ivshmem.size else 4194304,
               params.ivshmem.name,))
        raise MistClearException

    return Mist(start, end, check_audit_log)