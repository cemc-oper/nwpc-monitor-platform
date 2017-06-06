import moment from 'moment'
moment.locale('zh-cn');

export class TimeUtil {
    static parseUTCTimeString(time_string){
        return moment(time_string+" +0000", "YYYY-MM-DD HH:mm:ss Z");
    }
    static parseDate(date){
        return moment(date);
    }
    static getNow(){
        return moment();
    }
    static getDelayTime(start_time, end_time) {
        return start_time.from(end_time);
    }
}