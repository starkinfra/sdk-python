#!/bin/bash

# it seems it does not work well if using echo for function return value, and calling inside $() (is a subprocess spawned?)
function wait_and_get_exit_codes() {
    children=("$@")
    EXIT_CODE=0
    for job in "${children[@]}"; do
       echo "PID => ${job}"
       CODE=0;
       wait ${job} || CODE=$?
       if [[ "${CODE}" != "0" ]]; then
           echo "At least one test failed with exit code => ${CODE}" ;
           EXIT_CODE=1;
       fi
   done
}

DIRN=$(dirname "$0");

commands=(
        "{ python -m unittest tests.sdk.testBalance; }"
        "{ python -m unittest tests.sdk.testCreditNote; }"
        "{ python -m unittest tests.sdk.testCreditNoteLog; }"
        "{ python -m unittest tests.sdk.testEvent; }"
        "{ python -m unittest tests.sdk.testIssuingAuthorization; }"
        "{ python -m unittest tests.sdk.testIssuingBalance; }"
        "{ python -m unittest tests.sdk.testIssuingBin; }"
        "{ python -m unittest tests.sdk.testIssuingCard; }"
        "{ python -m unittest tests.sdk.testIssuingCardLog; }"
        "{ python -m unittest tests.sdk.testIssuingHolder; }"
        "{ python -m unittest tests.sdk.testIssuingHolderLog; }"
        "{ python -m unittest tests.sdk.testIssuingInvoice; }"
        "{ python -m unittest tests.sdk.testIssuingInvoiceLog; }"
        "{ python -m unittest tests.sdk.testIssuingPurchase; }"
        "{ python -m unittest tests.sdk.testIssuingPurchaseLog; }"
        "{ python -m unittest tests.sdk.testIssuingTransaction; }"
        "{ python -m unittest tests.sdk.testIssuingWithdrawal; }"
        "{ python -m unittest tests.sdk.testKey; }"
        "{ python -m unittest tests.sdk.testPixRequest; }"
        "{ python -m unittest tests.sdk.testPixRequestLog; }"
        "{ python -m unittest tests.sdk.testPixReversal; }"
        "{ python -m unittest tests.sdk.testPixReversalLog; }"
        "{ python -m unittest tests.sdk.testPixStatement; }"
    )

clen=`expr "${#commands[@]}" - 1` # get length of commands - 1

children_pids=()
for i in `seq 0 "$clen"`; do
    (echo "${commands[$i]}" | bash) &   # run the command via bash in subshell
    children_pids+=("$!")
    echo "$i ith command has been issued as a background job"
done
# wait; # wait for all subshells to finish - its still valid to wait for all jobs to finish, before processing any exit-codes if we wanted to
#EXIT_CODE=0;  # exit code of overall script
wait_and_get_exit_codes "${children_pids[@]}"

echo "EXIT_CODE => $EXIT_CODE"
sleep 5
exit "$EXIT_CODE"
# end
