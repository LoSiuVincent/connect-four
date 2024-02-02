export class Subject {
    constructor() {
        this.callbacks = [];
    }

    addListener(event, listener) {
        this.callbacks.push([event, listener]);
    }

    async notify(event, data) {

        const promises = [];

        this.callbacks.forEach((eventCallbackTuple) => {
            const listenEvent = eventCallbackTuple[0];
            const listener = eventCallbackTuple[1];
            if (event === listenEvent) {
                const updatePromise = listener.update(data);
                promises.push(updatePromise);
            }
        });

        return Promise.all(promises);
    }
}