-- select * from hawktracker.comment;
DELETE FROM hawktracker.comment;

-- DROP TABLE hawktracker.comment;
-- Reset the sequence for the id columnhawktracker
ALTER SEQUENCE hawktracker.comment_id_comment_seq RESTART;


select * from hawktracker.comment;

UPDATE hawktracker.issue
SET expected_completion	 = NULL;

CREATE TABLE hawktracker.comment (
    id_comment SERIAL PRIMARY KEY ,
    issue_id INT,
    date_posted DATE,
    email TEXT,
    comment TEXT,
    remarks TEXT,
    image_paths TEXT[],
    FOREIGN KEY (issue_id) REFERENCES hawktracker.issue(id)
);

ALTER TABLE hawktracker.issue
ADD COLUMN tags TEXT[];

UPDATE hawktracker.issue
SET tags = ARRAY[]::TEXT[];


-- Inserting multiple tags for a row
UPDATE hawktracker.issue
SET tags = ARRAY['Bug', 'Feature', 'Performance'];
-- WHERE your_condition;


-- check if tag EXISTS
SELECT * FROM your_table_name WHERE tags @> ARRAY['Bug'];



COPY (SELECT * FROM hawktracker.issue) TO 'request_status.csv' WITH CSV HEADER;


COPY (SELECT * FROM hawktracker.issue) TO PROGRAM 'cat > /request_status.csv' WITH CSV HEADER;






CREATE SCHEMA HawkTracker;

DELETE FROM hawktracker.comment;

SELECT * FROM  hawktracker.comment

DROP TYPE status;


-- Move the table from "public" to "new_schema"
ALTER TABLE public.request SET SCHEMA hawktracker;


\dt public.*
\dt hawktracker.*


 CREATE TYPE "URGENCY" AS ENUM ('LOW', 'MEDIUM', 'HIGH');

 CREATE TABLE hawktracker.issue (                                     
    id SERIAL PRIMARY KEY,
    date_posted DATE,
    urgency "URGENCY",
    issue VARCHAR(250),
    email TEXT,
    remarks VARCHAR(150),
    date_updated DATE,
    status "STATUS",
    expected_completion DATE
);

 CREATE TYPE "STATUS" AS ENUM ('OPEN', 'DEVELOPING', 'CLOSED');




DROP TABLE hawktracker.comment

-- CHANGE DATATYPE 
ALTER TABLE hawktracker.request
ALTER COLUMN remarks TYPE TEXT;



CREATE TABLE hawktracker.issue AS
SELECT id, "URGENCY", date_posted, issue, email, remarks, date_updated, "STATUS", expected_completion 
FROM issue;

ALTER TABLE hawktracker.issue
DROP COLUMN urgency,
DROP COLUMN status;

ALTER TABLE hawktracker.issue
ADD COLUMN urgency "URGENCY",
ADD COLUMN status "STATUS";

SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'hawktracker' AND table_name = 'comment';

-- select * from hawktracker.issue;
DELETE FROM hawktracker.issue;



-- Reset the sequence for the id columnhawktracker
ALTER SEQUENCE hawktracker.id_comment RESTART;


SELECT enumlabel
FROM pg_enum
WHERE enumtypid = 'URGENCY' ::regtype;



/*markdown
### CHECK ENUM DEFINITIONS
*/

SELECT typname, enumlabel FROM pg_enum
JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
WHERE typname = 'STATUS';

-- Step 1: Add the primary key constraint
ALTER TABLE hawktracker.issue
ADD CONSTRAINT issue_id PRIMARY KEY (id);


-- CHECK FOR FOREIGN KEYS
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    a.attname AS column_name,
    confrelid::regclass AS referenced_table_name,
    af.attname AS referenced_column_name
FROM
    pg_constraint AS c
    JOIN pg_attribute AS a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
    JOIN pg_attribute AS af ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid
WHERE
    conrelid::regclass = 'hawktracker.comment'::regclass
    AND contype = 'f';


SELECT column_name
FROM information_schema.key_column_usage
WHERE table_schema = 'hawktracker'
  AND table_name = 'issue'
  AND constraint_name = 'issue_id';


SELECT *
FROM information_schema.table_constraints
WHERE constraint_name = 'id_comment'
  AND table_schema = 'hawktracker'
  AND table_name = 'comment';



DELETE from hawktracker.comment

-- Reset the sequence for the id columnhawktracker
ALTER SEQUENCE hawktracker.comment_id_comment_seq RESTART;

ALTER SEQUENCE hawktracker.id_comment RESTART WITH 1;


UPDATE hawktracker.issue
SET status = 'OPEN';

SELECT * from hawktracker.issue

INSERT INTO hawktracker.issue (date_posted, urgency, issue ,email, status)
VALUES ( CURRENT_DATE , 'MEDIUM', 'Commit Test', null, 'OPEN');

DELETE FROM hawktracker.issue WHERE id = 40;

INSERT INTO hawktracker.issue (date_posted, urgency, issue ,email)
VALUES ( CURRENT_DATE , 'MEDIUM', 'Hourly data are late', null),
       ( CURRENT_DATE , 'LOW', 'More slicers/ filters required. ', null),
      ( CURRENT_DATE , 'HIGH', 'Date/Time/MNO filter not working on all graphs', 'louis.lee.shao.jun@ericsson.com');


INSERT INTO hawktracker.issue (date_posted, urgency, issue ,email)
VALUES ( CURRENT_DATE , 'HIGH', 'UL User Thpt - not correct in hourly Chart', null),
       ( CURRENT_DATE , 'HIGH', 'Latency - Radio interface -not correct in hourly chart', null),
       ( CURRENT_DATE , 'MEDIUM', 'ERAB drop rate  Formula need to check', null),
       ( CURRENT_DATE , 'HIGH', 'UL data Volum -Not correct in daily data', null),
       ( CURRENT_DATE , 'HIGH', 'DL User Thpt not correct in daily Data', null),
       ( CURRENT_DATE , 'MEDIUM', 'Slicer required Date ,Hour', null),
       ( CURRENT_DATE , 'MEDIUM', 'Slicer Node or cell level', null),
       ( CURRENT_DATE , 'MEDIUM', 'Can be inter bunch of sites and get output', null),
       ( CURRENT_DATE , 'HIGH', 'Cluster Slicer not working', null),
       ( CURRENT_DATE , 'MEDIUM', 'Region /cluster/state/CUPS /mno wise mapping', null),
       ( CURRENT_DATE , 'MEDIUM', 'Enable filtering/selection for multiple sites and cells for hourly and daily', 'kong.yew.chan@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Enable Multiple windows open with different regions for viewing', 'kong.yew.chan@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'LTE Flex dont have inter freq Prep/Exec SR', 'huzaifah.bin.shahrul.bashah@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'system "feteching time" is india time zone, properly malaysia time will be better', 'hoong.yong.chin@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'suggest to load 7 or 14 days data to make it load faster in platform', 'hoong.yong.chin@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Customised Cells doest not support wild card filter/searching', 'hoong.yong.chin@ericsson.com'),
       ( CURRENT_DATE , 'LOW', 'Suggest Diff Chart color for both NR and LTE chart', 'hoong.yong.chin@ericsson.com'),
       ( CURRENT_DATE , 'HIGH', 'Cell Level > Daily .  NR UL RSSI is missing', 'huzaifah.bin.shahrul.bashah@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Filter by Morphology', 'shahrul.mohd.appandi@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Wildcard in customized sites', 'louis.lee.shao.jun@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Monthly and Weekly Performance', 'chin.han.lim@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Report export', 'chin.han.lim@ericsson.com'),
       ( CURRENT_DATE , 'HIGH', 'Hourly KPI DL and UL User thpt are incorrect (mismatch) e.g. Sabah and Sarawak region', 'kong.yew.chan@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'To show OB sites counts  for each region', 'kong.yew.chan@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'To add report IFHO', 'shahrul.mohd.appandi@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Possible to hide MNO filtering so that when take a snip, doesnt show other MNOs', 'mufaddal.abbas.bhai@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Possible to show multiple cell level (separate lines in 1 graph)', 'mufaddal.abbas.bhai@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Possible to add IFO Prep & Exec, SPIFHO Prep & Exec, and IFO Prep & Exec in the LTE Cell Level & also PLMN Level', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'LOW', 'Possible to show formula been used when we move the cursor towards the KPI name/any way to show what formula been used for each KPI', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'LOW', 'Possible to use normal standard Capital Letter for the beginning of the KPI Name; eg Interfreq_HO instead of interfreq_ho. Just suggesting..Sorry for my bad OCD =)', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'HIGH', 'Some KPI shows 0.99, some KPI shows in percentage 99%, some % can even show 100.02%, some are using 99.232%, and some % can go up to 160%. Can we standardize this % range?', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Possible to show formula been used when we move the cursor towards the KPI name/any way to show what formula been used for each KPI', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'Can show which unit been used; MB or GB especially for traffic?', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'HIGH', 'LTE & NR DL_BLER is missing. Possible to add in?', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'MEDIUM', 'In NR Modulation, the range is weird, 0.00M. NR Modulation looks fine', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com'),
       ( CURRENT_DATE , 'LOW', 'Possible for Flex level, the KPI line to follow MNOs colour', 'saffiq.azidi.bin.mohd.suhaimi@ericsson.com')
      ;

CREATE TABLE hawktracker.comment (
    id_comment SERIAL PRIMARY KEY ,
    issue_id INT,
    date_posted DATE,
    email TEXT,
    issue TEXT,
    remarks TEXT,
    FOREIGN KEY (issue_id) REFERENCES hawktracker.issue(id)
);

 CREATE TABLE hawktracker.issue (                                     
    id SERIAL PRIMARY KEY,
    date_posted DATE,
    urgency "URGENCY",
    issue TEXT,
    email TEXT,
    remarks TEXT,
    date_updated DATE,
    status "STATUS",
    expected_completion DATE
);

SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'issue';


SELECT * FROM hawktracker.comment

INSERT INTO hawktracker.comment (issue_id, date_posted, email , issue, remarks)
VALUES ( 1 ,  CURRENT_DATE, 'test@ericsson.com', 'comment issue 2', 'comment remarks 2');