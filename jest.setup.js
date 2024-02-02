import jQuery from 'jquery';
import nodeFetch from 'node-fetch'
import { TextEncoder, TextDecoder } from 'util';

global.jQuery = global.$ = jQuery;
if (!global.fetch) {
    global.fetch = nodeFetch;
}

Object.assign(global, { TextDecoder, TextEncoder });