#ifndef ARTUCLE_ANALYSIS_ANALYST_IMPL__FAKE_ANALYST_H_
#define ARTUCLE_ANALYSIS_ANALYST_IMPL__FAKE_ANALYST_H_


#include "analyst/i_analyst.h"
#include "miner/miner.h"
#include "utils/options.h"


namespace analyst {

namespace impl_ {


class FakeAnalystOptions : public utils::AOptionCollection {
 public:
  FakeAnalystOptions();
};


class FakeAnalyst : public IAnalyst {
 public:
  FakeAnalyst(miner::Miner* miner, FakeAnalystOptions const& opt);

  DocRelInfo GetDocRelInfo(DocIdentity const& id) const override final;
};

}  // namespace impl_

}  // namespace analyst

#endif  // ARTUCLE_ANALYSIS_ANALYST_IMPL__FAKE_ANALYST_H_

