export class Util {
    static getTimeInterval(start_date, end_date) {
        let ms_interval = end_date.getTime() - start_date.getTime();
        let days = Math.floor(ms_interval / (24 * 3600 * 1000));

        let leave1 = ms_interval % (24 * 3600 * 1000);    //计算天数后剩余的毫秒数
        let hours = Math.floor(leave1 / (3600 * 1000));

        let leave2 = leave1 % (3600 * 1000);      //计算小时数后剩余的毫秒数
        let minutes = Math.floor(leave2 / (60 * 1000));

        let leave3 = leave2 % (60 * 1000);     //计算分钟数后剩余的毫秒数
        let seconds = Math.round(leave3 / 1000);

        return {
            days: days,
            hours: hours,
            minutes: minutes,
            seconds: seconds
        }
    }

    static getDelayTime(start_time, end_time) {
        let repo_delay = Util.getTimeInterval(start_time, end_time);
        if (repo_delay.days) {
            return repo_delay.days + '天前';
        } else if (repo_delay.hours) {
            return repo_delay.hours + '小时前';
        } else if (repo_delay.minutes) {
            return repo_delay.minutes + '分钟前';
        } else if (repo_delay.seconds) {
            return repo_delay.seconds + '秒前';
        }
        return "";
    }
}