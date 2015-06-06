/**
 * Created by bergus on 15-5-27.
 */


$.validator.addMethod("show_error", function (value, element, param) {
    var length = param.length;
    if (length > 0) {
        console.log(param)
        return false
    }
    return true;
}, $.validator.format("{0}"));
