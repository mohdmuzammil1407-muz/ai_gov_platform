# STAFF REGISTRATION SYSTEM - ARCHITECTURE & FLOW

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     ADMIN DASHBOARD                             │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Admin User Interface                                    │   │
│  │                                                          │   │
│  │  [Register New Staff Button] ─────────────────┐         │   │
│  └──────────────────────────────────────────────┼──────────┘   │
│                                                   │               │
│                                                   ▼               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  StaffRegistrationModal Component                       │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ Form Fields:                                       │ │   │
│  │  │  • Name (text input)                               │ │   │
│  │  │  • Email (text input) → Email Validation         │ │   │
│  │  │  • Password (password) → Strength Check          │ │   │
│  │  │  • Confirm Password (password) → Match Check    │ │   │
│  │  │  • Department (dropdown) → Whitelist Check      │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │                                                          │   │
│  │  [Cancel Button] [Register Staff Button]               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ (Form Data + JWT Token)
                              ▼
        ┌─────────────────────────────────────┐
        │  API Request                         │
        │  POST /api/staff/register           │
        │                                      │
        │  Headers:                           │
        │  - Authorization: Bearer <JWT>     │
        │  - Content-Type: application/json  │
        │                                      │
        │  Body:                              │
        │  {                                  │
        │    name: "John Doe",                │
        │    email: "john@ex.com",            │
        │    password: "Test123",             │
        │    department: "Health"             │
        │  }                                  │
        └─────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (Flask)                             │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  @jwt_required(required_role="admin")                   │   │
│  │  POST /api/staff/register                              │   │
│  │                                                          │   │
│  │  1. Validate Admin Authorization                       │   │
│  │     ✓ JWT token valid?                                │   │
│  │     ✓ Role = "admin"?                                 │   │
│  │                                                          │   │
│  │  2. Extract & Sanitize Input                          │   │
│  │     ✓ Trim whitespace                                 │   │
│  │     ✓ Lowercase email                                │   │
│  │     ✓ Strip special characters                        │   │
│  │                                                          │   │
│  │  3. Validate All Fields                               │   │
│  │     ✓ Name required & non-empty                       │   │
│  │     ✓ Email format (regex)                            │   │
│  │     ✓ Password strength:                              │   │
│  │       - 6+ characters                                │   │
│  │       - 1 uppercase letter                           │   │
│  │       - 1 number                                     │   │
│  │     ✓ Department in ALLOWED_DEPARTMENTS             │   │
│  │                                                          │   │
│  │  4. Check Duplicate Email                            │   │
│  │     ✓ Query: users.findOne({email: email})          │   │
│  │     ✓ If exists → Return 409 Conflict               │   │
│  │                                                          │   │
│  │  5. Hash Password                                    │   │
│  │     ✓ hash_password(password)                        │   │
│  │     ✓ Uses werkzeug.security (pbkdf2)               │   │
│  │                                                          │   │
│  │  6. Create Staff Document                           │   │
│  │     {                                                │   │
│  │       user_id: uuid,                                │   │
│  │       name: "John Doe",                            │   │
│  │       email: "john@ex.com",                        │   │
│  │       password: "hashed_password",                │   │
│  │       role: "staff",                              │   │
│  │       department: "Health",                       │   │
│  │       created_at: timestamp,                      │   │
│  │       is_active: true                            │   │
│  │     }                                              │   │
│  │                                                          │   │
│  │  7. Insert to Database                            │   │
│  │     ✓ MongoDB: users_collection.insert_one()      │   │
│  │                                                          │   │
│  │  8. Return Success (201)                          │   │
│  │     {                                              │   │
│  │       message: "Staff registered successfully",   │   │
│  │       staff_id: uuid,                            │   │
│  │       email: "john@ex.com",                      │   │
│  │       name: "John Doe",                         │   │
│  │       department: "Health",                     │   │
│  │       role: "staff"                            │   │
│  │     }                                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ (Success Response)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FRONTEND - Response Handling                   │
│                                                                   │
│  ✓ Set success = true                                           │
│  ✓ Show green success notification                              │
│  ✓ Display staff details: "John Doe (john@ex.com) can now      │
│    log in as staff in the Health department"                   │
│  ✓ Wait 2 seconds                                               │
│  ✓ Auto-close modal                                             │
│  ✓ Clear form data                                              │
│  ✓ Notification auto-clears after 3 seconds                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Validation Flow Diagram

```
┌─── FRONTEND VALIDATION ───┐
│                            │
│  Input Form Data           │
│      │                     │
│      ▼                     │
│  Required Fields?          │
│  ├─ No  → Error message   │
│  └─ Yes ▼                 │
│      Name OK?             │
│      ├─ No  → Error msg   │
│      └─ Yes ▼             │
│      Email Format?        │
│      ├─ No  → Error msg   │
│      └─ Yes ▼             │
│      Password OK?         │
│      ├─ No  → Error msg   │
│      └─ Yes ▼             │
│      Passwords Match?     │
│      ├─ No  → Error msg   │
│      └─ Yes ▼             │
│      Department OK?       │
│      ├─ No  → Error msg   │
│      └─ Yes ▼             │
│  Submit to Backend        │
│                            │
└────────────────────────────┘
            │
            ▼
┌─── BACKEND VALIDATION ───┐
│                           │
│  Receive Request          │
│      │                    │
│      ▼                    │
│  Admin JWT Valid?         │
│  ├─ No  → 403 Forbidden  │
│  └─ Yes ▼                │
│  Name Required?           │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Email Required?          │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Email Format Valid?      │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Password Required?       │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Password 6+ chars?       │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Password has uppercase?  │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Password has number?     │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Department Required?     │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Dept in Whitelist?       │
│  ├─ No  → 400 Bad Req    │
│  └─ Yes ▼                │
│  Email Already Used?      │
│  ├─ Yes → 409 Conflict   │
│  └─ No  ▼                │
│  Hash Password            │
│      │                    │
│      ▼                    │
│  Create Document          │
│      │                    │
│      ▼                    │
│  Insert to DB             │
│      │                    │
│      ▼                    │
│  201 Created              │
│                           │
└───────────────────────────┘
```

---

## New Staff Login Flow

```
┌─────────────────────────────────────────────────┐
│           STAFF LOGIN PAGE                      │
│                                                  │
│  Email:    [john@ex.com...................]     │
│  Password: [***..............................]   │
│                                                  │
│           [Login Button]                        │
└─────────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  POST /api/login           │
        │  {                         │
        │    email: "john@ex.com",   │
        │    password: "Test123"     │
        │  }                         │
        └────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│          BACKEND LOGIN ENDPOINT                 │
│                                                  │
│  1. Find user by email                         │
│  2. Verify password hash                       │
│     verify_password("Test123", stored_hash)    │
│  3. Generate JWT payload:                      │
│     {                                           │
│       user_id: "uuid",                         │
│       role: "staff",                           │
│       department: "Health",  ← KEY!            │
│       exp: future_time                        │
│     }                                           │
│  4. Return 200 with JWT                        │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│        FRONTEND RECEIVES TOKEN                  │
│                                                  │
│  1. Extract token from response                │
│  2. Store in localStorage                      │
│  3. Decode JWT payload                         │
│  4. Store user info                            │
│  5. Redirect to dashboard based on role        │
│     if role === "staff" → /staff/dashboard     │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│        STAFF DASHBOARD                         │
│                                                  │
│  Welcome, John Doe (staff)                    │
│  Department: Health                            │
│                                                  │
│  Your Complaints (Health dept only):          │
│  1. Hospital waiting times - In Progress      │
│  2. Medicine shortage - Submitted             │
│  3. Staff shortage - Resolved                 │
│                                                  │
│  [Update Status] buttons available             │
└─────────────────────────────────────────────────┘
```

---

## Database Schema

```
┌─ USERS COLLECTION ────────────────────────────────┐
│                                                    │
│  Admin User:                                      │
│  {                                                │
│    _id: ObjectId(...),                           │
│    user_id: "uuid-admin",                        │
│    email: "admin@ex.com",                        │
│    password: "pbkdf2:sha256:...",  ← HASHED     │
│    role: "admin",                                │
│    department: null,                             │
│    created_at: ISODate(...),                    │
│    is_active: true                              │
│  }                                               │
│                                                   │
│  Staff User (After Registration):               │
│  {                                               │
│    _id: ObjectId(...),                          │
│    user_id: "uuid-staff",                       │
│    email: "john@ex.com",     ← LOWERCASE       │
│    password: "pbkdf2:sha256:...",  ← HASHED   │
│    name: "John Doe",                            │
│    role: "staff",                               │
│    department: "Health",     ← FROM DROPDOWN   │
│    created_at: ISODate(...),                   │
│    is_active: true           ← NEW FIELD      │
│  }                                              │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Error Handling Tree

```
Request to /api/staff/register
    │
    ├─ No JWT token?
    │  └─ 401 Unauthorized
    │
    ├─ JWT invalid?
    │  └─ 401 Unauthorized
    │
    ├─ Role ≠ "admin"?
    │  └─ 403 Forbidden
    │
    ├─ JSON parse error?
    │  └─ 400 Bad Request
    │
    ├─ name empty?
    │  └─ 400 + "Name is required"
    │
    ├─ email empty?
    │  └─ 400 + "Email is required"
    │
    ├─ email format invalid?
    │  └─ 400 + "Invalid email format"
    │
    ├─ password empty?
    │  └─ 400 + "Password is required"
    │
    ├─ password < 6 chars?
    │  └─ 400 + "Password must be at least 6 characters"
    │
    ├─ no uppercase in password?
    │  └─ 400 + "Password must contain at least one uppercase letter"
    │
    ├─ no digit in password?
    │  └─ 400 + "Password must contain at least one number"
    │
    ├─ department empty?
    │  └─ 400 + "Department is required"
    │
    ├─ department not in whitelist?
    │  └─ 400 + "Invalid department. Allowed: ..."
    │
    ├─ email already exists?
    │  └─ 409 Conflict + "Email already registered"
    │
    ├─ database error?
    │  └─ 500 + "Database error: ..."
    │
    └─ ✓ All validation passed?
       └─ 201 Created + staff details
```

---

## File Dependencies

```
Admin Dashboard
    │
    ├─ imports: StaffRegistrationModal
    │
    └─ imports: registerStaff (from api)
            │
            └─ calls: api.post("/staff/register")
                    │
                    └─ Backend: POST /api/staff/register
                            │
                            ├─ validates: email, password, department
                            ├─ hashes: password (werkzeug.security)
                            ├─ checks: duplicate email in MongoDB
                            └─ creates: staff document in users collection
```

---

## Component Props & Data Flow

```
AdminDashboard
├─ State: showStaffRegistration (boolean)
├─ State: registrationSuccess (object or null)
│
├─ Handler: handleRegistrationSuccess(staffData)
│   └─ Set registrationSuccess state
│   └─ Auto-clear after 3 seconds
│
└─ Render: <StaffRegistrationModal
    isOpen={showStaffRegistration}
    onClose={() => setShowStaffRegistration(false)}
    onSuccess={handleRegistrationSuccess}
  />

StaffRegistrationModal
├─ Props:
│   ├─ isOpen (boolean)
│   ├─ onClose (function)
│   └─ onSuccess (function)
│
├─ State: form (name, email, password, confirmPassword, department)
├─ State: loading (boolean)
├─ State: error (string)
├─ State: success (boolean)
│
├─ Handler: handleSubmit
│   ├─ Validate form
│   ├─ Set loading = true
│   ├─ Call registerStaff(form)
│   ├─ Handle response
│   ├─ Call onSuccess(response)
│   └─ Set loading = false
│
└─ Render: Modal with form fields
```

This architecture ensures secure, validated staff registration with proper error handling and user feedback at every step.
