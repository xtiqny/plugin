## holidays

**Author:** xtiqny
**Version:** 0.0.1
**Type:** tool

### Description

A Chinese holiday query tool powered by the timor.tech API. This plugin allows you to check whether a specific date is a holiday, a compensatory workday, or a regular working day in China.

#### Features

- **Holiday Detection**: Identify statutory holidays in China
- **Compensatory Workday Recognition**: Detect adjusted workdays (make-up days for holidays)
- **Weekend Detection**: Distinguish between regular weekends and weekdays

#### Usage Example

Date format: `2026-07-31` or `2026-7-31`

**Response Fields:**
- `date`: The queried date
- `is_holiday`: Whether the date is a holiday (true/false)
- `holiday_name`: Name of the holiday (e.g., "National Day")
- `wage`: Overtime pay multiplier
- `rest_days`: Remaining days of the holiday
- `week_type`: Day of the week in Chinese (e.g., "周五" for Friday)
- `week_number`: Day of the week as a number (1-7)
- `type`: Date type (holiday/normal/workday)

#### Technical Details

- **Data Source**: [timor.tech](https://timor.tech/api/holiday) Holiday API
- **Supported Years**: 2024-2026 holiday data
- **Request Method**: HTTP GET
- **Response Format**: JSON

#### Use Cases

- Workflow automation to check if a date is a working day
- Scheduling systems to identify holidays and compensatory days
- Cron jobs to skip execution on holidays
- Attendance systems to calculate working days

#### Notes

1. Date format supports both `YYYY-MM-DD` and `YYYY-M-D`
2. API returns data including both lunar and Gregorian calendar holidays
3. Compensatory workdays (adjusted working days) are marked as `workday` type
