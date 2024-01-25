DO
$$

--  Single Migration script between checkpoint and tutoring
--  Run this script in checkpoint/aureos and then copy "print" statements to tutoring

    DECLARE
        record_data            RECORD;
        tutor_login            TEXT;
        tutee_login            TEXT;
        meeting_date           DATE;
        label                  TEXT;
        ac_year                TEXT;
        updated_by             TEXT;
        updated                DATE;
        sql_insert_pt_tutoring TEXT;
        sql_values             TEXT;

    BEGIN

        sql_insert_pt_tutoring :=
                'INSERT INTO personal_tutoring_meeting (year, tutor_login,tutee_login,label,meeting_date,updated_by,updated ) values(';
        RAISE NOTICE '';
        FOR record_data IN select title, tutor, tutee, year, date from pt_meeting
            LOOP
                tutor_login := quote_literal(record_data.tutor);
                tutee_login := quote_literal(record_data.tutee);
                ac_year := quote_literal(record_data.year);
                label := quote_literal(record_data.title);
                meeting_date := quote_literal(record_data.date);
                updated_by := quote_nullable('edtech');
                updated := quote_literal(record_data.date);

                sql_values := ac_year || ', ' || tutor_login || ', ' || tutee_login || ', ' || label || ', ' ||
                              quote_literal(meeting_date) ||
                              ', ' || updated_by || ', ' || quote_literal(updated);
                RAISE NOTICE '%', sql_insert_pt_tutoring || sql_values || ');';
            END LOOP;
    END

$$;