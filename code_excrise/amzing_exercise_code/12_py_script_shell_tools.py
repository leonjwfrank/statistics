import getopt
import sys


def CreateRoom(values=None):
    cre_snap = ApiRefRoom.ApiCreateRoom()
    if values:
        map(lambda (key, value): setattr(cre_room, key, value), values.items())
    req_resp = Request.send_post(cre_room)
    return req_resp


class call_module_api(object):
    def ret_use_age(self):
        print("Usage:%s [-h|-c|-p] [--help|--call|--params] args...." % sys.argv[0])
        print(' -h | --help help \n' \
              ' -c | --call, call api by bvt, params would be like: -c|--call=GetV \n' \
              ' -p | --params, params like: -p|--params=Id:1-2-3,Az:test\n')

    def ret_check_arg(self):
        name, params = '', ''
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hc:p:", ["help", "call=", "params="])

            print("============ opts ==================")
            print(opts)

            print("============ args ==================")
            print(args)

            # check all param
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    self.ret_use_age()
                    sys.exit(1)
                if opt in ("-c", "--call"):
                    name = arg
                elif opt in ("-p", "--params"):
                    params = arg
                else:
                    print("%s  ==> %s" % (opt, arg))
                    raise AssertionError("sys args {}".format(opts, args))
                if name and params:
                    return [name, params]
        except getopt.GetoptError:
            print("getopt error!")
            self.ret_use_age()
            sys.exit(1)

    def ret_api_info(self):
        ck_args = self.ret_check_arg()
        api_name = ck_args[0]
        json = ck_args[1]
        return [api_name, json]


def ret_api_call_list(api_name, json_value):
    all_api = globals().keys()
    json_p = {}
    if str(api_name) not in str(all_api):
        raise AssertionError("This {} not define in V".format(str(api_name)))

    if ',' in str(json_value):
        param_list = str(json_value).split(',')
        for param in param_list:
            json_p[str(param).split(':')[0]] = str(param).split(':')[1]
    else:
        json_p[str(json_value).split(':')[0]] = str(json_value).split(':')[1]

    for na in all_api:
        if "main" != str(na) and "ret" not in str(na):
            if str(na) == str(api_name):
                api_call = globals().get(api_name)
                print("Call  {}, params {}".format(api_name, json_p))
                call_resp = api_call(json_p)

                return call_resp
    print("Not match this {} in this module".format(api_name))

def main():
    _sys_api_info = call_module_api().ret_info()
    name = _sys_api_info[0]
    param = _sys_api_info[1]
    return ret_api_call_list(name, param)

if __name__ == '__main__':

    p_url = 'http://127.0.0.1:8889/ws/'
    p_region = 'ph-mnl'
    p_access_id = 'user_admin'
    p_access_key = 'O78sMTX8K9em1YNj3zo20w=='

    params_list = {"Full": "true",
                   "RoomId": "cF6i5N38AuNKTOKuOZYshlxt1234",
                   "Timestamp": "1548743322588",
                   "Version": "1.0.0",
                   "TracebakcId": "CreateSnapshot_45253624802",
                   "Timeout": "70000",
                   "Signature": "F6i5N38AuNKasdwaqwSDAwdlxt67kw=",
                   "UserId": "100262-83597"}
    request = Request(p_url, p_region, p_access_id, p_access_key)
    sign_string = service.generate_to_sign_string(params=params_list, method='POST')
    sign_value = service.sign(params=params_list, method='POST', secret_key=p_access_key)
    print("string:{}".format(sign_string))
    print("value:{}".format(sign_value))

    new_dev_id = ret_new_id()
    resp_info = main()