import { Subject } from "subject.js";
import { jest, expect, describe, test } from "@jest/globals";

test("subject should notify to the observers", async () => {
    const subject = new Subject();

    const listenerOne = { update: jest.fn() };
    const listenerTwo = { update: jest.fn() };
    const listenerThree = { update: jest.fn() };
    subject.addListener("eventOne", listenerOne);
    subject.addListener("eventTwo", listenerTwo);
    subject.addListener("eventThree", listenerThree);

    await subject.notify("eventOne", { a: 1, b: 2 });
    await subject.notify("eventTwo", { a: 10, b: 20 });

    expect(listenerOne.update).toHaveBeenCalledWith("eventOne", { a: 1, b: 2 });
    expect(listenerTwo.update).toHaveBeenCalledWith("eventTwo", { a: 10, b: 20 });
    expect(listenerThree.update).not.toHaveBeenCalled();
});