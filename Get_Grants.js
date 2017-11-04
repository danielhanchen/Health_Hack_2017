const mongoose = require('mongoose');
const { Schema } = mongoose;

const grantSchema = new Schema({
  index: {
    type: String,
    trim: true
  },
  agency: {
    type: String
  },
  category: {
    type: [String]
  },
  deadline: {
    type: String
  },
  description: {
    type: String
  },
  eligibility: {
    type: String
  },
  email: {
    type: String
  },
  estimated_grant_value: {
    type: Number
  },
  from_where: {
    type: String
  },
  go_id: {
    type: String
  },
  instructions_for_lodgement: {
    type: String
  },
  internal_reference_id: {
    type: String
  },
  new_grants: {
    type: Number
  },
  publish_date: {
    type: String
  },
  site: {
    type: String
  },
  title: {
    type: String
  },
  total_grant_amount: {
    type: String
  }
});

const Grant = mongoose.model('Grants', grantSchema);

module.exports = Grant;
