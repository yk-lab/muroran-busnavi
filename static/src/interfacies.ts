interface IStop {
    id: string;
    wheelchair_boarding: number;
    start_date: string;
    end_date: string;
    name: any;
    positions: any;
    url: any;
}

interface IStopName {
    id: string;
    stop_code: string;
    name: string;
    desc: string;
    start_date: string;
    end_date: string;
}

interface IStopPosition {
    id: string;
    stop_code: string;
    subname: string;
    desc: string;
    lat: number;
    lng: number;
    geohash: string;
    quadkey: string;
    start_date: string;
    end_date: string;
}

interface IStopUrl {
    id: string;
    stop_code: string;
    url: string;
    start_date: string;
    end_date: string;
}
