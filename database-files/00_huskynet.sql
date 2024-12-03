DROP DATABASE IF EXISTS huskynet;

CREATE DATABASE huskynet;

USE huskynet;

# ---------------------------------------------------------------------- #
# Add table "Job"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Job (
  JobID VARCHAR(50) NOT NULL,
  Title VARCHAR(75) NOT NULL,
  Description VARCHAR(1000),
  Status VARCHAR(100),
  PRIMARY KEY (JobID)

);

CREATE INDEX job_id ON Job (JobID);


# ---------------------------------------------------------------------- #
# Add table "Trait"                                              #
# ---------------------------------------------------------------------- #

CREATE TABLE Trait (
  TraitID VARCHAR(50) NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Description VARCHAR(1000),
  PRIMARY KEY (TraitID)

);

CREATE INDEX trait_id ON Trait (TraitID);

# ---------------------------------------------------------------------- #
# Add table "Candidate"                                              #
# ---------------------------------------------------------------------- #

CREATE TABLE Candidate (
  CandidateID VARCHAR(50) NOT NULL,
  Name VARCHAR(50) NOT NULL,
  InterviewNotes VARCHAR(1000),
  Status VARCHAR(50),
  Qualitites VARCHAR(1000),
  PRIMARY KEY (CandidateID)

);

CREATE INDEX candidate_id ON Candidate (CandidateID);

# ---------------------------------------------------------------------- #
# Add table "HiringUser"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE HiringUser (
  UserID VARCHAR(50) NOT NULL,
  Name VARCHAR(50),
  Role VARCHAR(50),

  PRIMARY KEY (UserID),
  CONSTRAINT fk_user FOREIGN KEY (UserID) REFERENCES Job(JobID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_user FOREIGN KEY (UserID) REFERENCES Candidate(CandidateID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX users_id ON HiringUser (UserID);

# ---------------------------------------------------------------------- #
# Add table "Engagement"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Engagement (
  EngagementID VARCHAR(50) NOT NULL,
  ConnectionsReq VARCHAR(50),
  ActiveUserCount INT,
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (EngagementID)
);

CREATE INDEX engagement_id ON Engagement (EngagementID);

# ---------------------------------------------------------------------- #
# Add table "Feedback"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Feedback (
  FeedbackID VARCHAR(50) NOT NULL,
  Content VARCHAR(2000),
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (FeedbackID)
);

CREATE INDEX feedback_id ON Feedback (FeedbackID);


# ---------------------------------------------------------------------- #
# Add table "PerformanceMetrics"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE PerformanceMetrics (
  MetricID VARCHAR(50) NOT NULL,
  ResponseTime TIME,
  Uptime TIME,
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (MetricID),
  CONSTRAINT fk_metrics FOREIGN KEY (MetricID) REFERENCES Engagement(EngagementID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX metric_id ON PerformanceMetrics(MetricID);


# ---------------------------------------------------------------------- #
# Add table "Feature"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Feature (
  FeatureID VARCHAR(50) NOT NULL,
  Name VARCHAR(2000),
  UserCount INT,
  PRIMARY KEY (FeatureID),
  CONSTRAINT fk_feature FOREIGN KEY (FeatureID) REFERENCES PerformanceMetrics(MetricID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_feature FOREIGN KEY (FeatureID) REFERENCES Feedback(FeedbackID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX feature_id ON Feature (FeatureID);

# ---------------------------------------------------------------------- #
# Add table "AnalyticsUser"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE AnalyticsUser (
  UserID VARCHAR(50) NOT NULL,
  Location VARCHAR(50),
  Major VARCHAR(50),

  PRIMARY KEY (UserID),
  CONSTRAINT fk_anauser FOREIGN KEY (UserID) REFERENCES Feedback(FeedbackID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_anauser FOREIGN KEY (UserID) REFERENCES Feature(FeatureID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk3_anauser FOREIGN KEY (UserID) REFERENCES Engagement(EngagementID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX anausers_id ON AnalyticsUser (UserID);

# ---------------------------------------------------------------------- #
# Add table "SearchFilters"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE SearchFilters (
  FilterID VARCHAR(50) NOT NULL,
  FilterType VARCHAR(50),
  PRIMARY KEY (FilterID)
);

CREATE INDEX filter_id ON SearchFilters(FilterID);


# ---------------------------------------------------------------------- #
# Add table "Skills"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Skills (
  SkillID VARCHAR(50) NOT NULL,
  SkillName VARCHAR(200),
  AlumniID INT,
  PRIMARY KEY (SkillID)

);

CREATE INDEX skills_id ON Skills(SkillID);

# ---------------------------------------------------------------------- #
# Add table "Messages"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Messages (
  MessageID VARCHAR(50) NOT NULL,
  SenderAlumniID INT,
  RecieverAlumniID INT,
  MessageContent VARCHAR(2000),
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (MessageID)

);

CREATE INDEX msgs_id ON Messages(MessageID);

# ---------------------------------------------------------------------- #
# Add table "WorkExperience"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE WorkExperience (
  ExperienceID VARCHAR(50) NOT NULL,
  AlumniID INT,
  Role VARCHAR(50),
  Company VARCHAR(50),
  StartDate DATE,
  EndDate DATE,
  IsCurrent BOOLEAN,
  PRIMARY KEY (ExperienceID)

);

CREATE INDEX work_id ON WorkExperience(ExperienceID);

# ---------------------------------------------------------------------- #
# Add table "Actions"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Actions (
  ActionID VARCHAR(50) NOT NULL,
  AlumniID INT,
  AdminID INT,
  ActionType VARCHAR(50),
  ActionTS VARCHAR(50),
  PRIMARY KEY (ActionID)

);

CREATE INDEX action_id ON Actions(ActionID);

# ---------------------------------------------------------------------- #
# Add table "Warnings"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Warnings (
  WarningID VARCHAR(50) NOT NULL,
  AlumniID INT,
  AdminID INT,
  Reason VARCHAR(500),
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (WarningID)

);

CREATE INDEX warn_id ON Warnings(WarningID);

# ---------------------------------------------------------------------- #
# Add table "Administrator"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Administrator (
  AdminID VARCHAR(50) NOT NULL,
  Name VARCHAR(50),
  Email VARCHAR(100),
  Role VARCHAR(100),
  PRIMARY KEY (AdminID),
  CONSTRAINT fk_admin FOREIGN KEY (AdminID) REFERENCES Warnings(WarningID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_admin FOREIGN KEY (AdminID) REFERENCES Actions(ActionID)
  ON UPDATE cascade ON DELETE restrict

);

CREATE INDEX admin_id ON Administrator(AdminID);


# ---------------------------------------------------------------------- #
# Add table "Alumni"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Alumni (
  AlumniID VARCHAR(50) NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Major VARCHAR(50) NOT NULL,
  AboutMe VARCHAR(2000),
  ProfilePic VARBINARY(10000),
  WorkExperience VARCHAR(2000),
  GradYear INT,
  PRIMARY KEY (AlumniID),
  CONSTRAINT fk2_alumni FOREIGN KEY (AlumniID) REFERENCES Messages(MessageID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk3_alumni FOREIGN KEY (AlumniID) REFERENCES WorkExperience(ExperienceID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk4_alumni FOREIGN KEY (AlumniID) REFERENCES Actions(ActionID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk5_alumni FOREIGN KEY (AlumniID) REFERENCES Warnings(WarningID)
  ON UPDATE cascade ON DELETE restrict

);

CREATE INDEX alumni_id ON Alumni(AlumniID);


#Bridge tables
# ---------------------------------------------------------------------- #
# Add table "Candidate_Traits"                                           #
# ---------------------------------------------------------------------- #

CREATE TABLE Candidate_Traits (
  CandidateID VARCHAR(50) NOT NULL,
  TraitID VARCHAR(50) NOT NULL,
  CONSTRAINT ct_pk PRIMARY KEY(CandidateID, TraitID),
  CONSTRAINT fk_ct FOREIGN KEY (CandidateID) REFERENCES Candidate(CandidateID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk_ct2 FOREIGN KEY (TraitID) REFERENCES Trait(TraitID)
  ON UPDATE cascade ON DELETE restrict
);

# ---------------------------------------------------------------------- #
# Add table "Alumni_Skills"                                           #
# ---------------------------------------------------------------------- #

CREATE TABLE Alumni_Skills (
  AlumniID VARCHAR(50) NOT NULL,
  SkillsID VARCHAR(50) NOT NULL,
  CONSTRAINT as_pk PRIMARY KEY(AlumniID, SkillsID),
  CONSTRAINT fk_as FOREIGN KEY (AlumniID) REFERENCES Alumni(AlumniID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk_as2 FOREIGN KEY (SkillsID) REFERENCES Skills(SkillID)
  ON UPDATE cascade ON DELETE restrict
);