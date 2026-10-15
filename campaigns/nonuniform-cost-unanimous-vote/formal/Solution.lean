module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace NonuniformCostUnanimousVote

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

def legalSource (x : List Nat) : Bool := x.all (fun w => w > 0)

def sourceWitness (x : List Nat) (subset : List Nat) : Bool :=
  decide subset.Nodup && subset.all (fun i => i < x.length) &&
  2 * (subset.map (fun i => x[i]?.getD 0)).sum == x.sum

def encodeSource := encodeList encodeNat

def validSourceOutput := searchOutput legalSource sourceWitness
def encodeInt (z : Int) : List Bool := [decide (z < 0)] ++ encodeNat z.natAbs
def encodeRat (q : Rat) : List Bool := encodeInt q.num ++ encodeNat q.den

abbrev Instance := List Rat × List Rat × Rat
def legalTarget (x : Instance) : Bool :=
  x.1.length == x.2.1.length && x.1.all (fun p => 0 < p && p < 1) && x.2.1.all (fun c => 0 < c)
def expectedCost (x : Instance) (order : List Nat) : Rat :=
  (order.zipIdx.map (fun (coin,j) =>
    let priorProbabilities := (order.take j).map (fun i => x.1[i]?.getD 0)
    (x.2.1[coin]?.getD 0) *
      (if j == 0 then 1 else priorProbabilities.prod + (priorProbabilities.map (1 - ·)).prod))).sum
def targetWitness (x : Instance) (order : List Nat) : Bool :=
  decide (order.Perm (List.range x.1.length)) && expectedCost x order ≤ x.2.2
def encodeTarget (x : Instance) := encodeList encodeRat x.1 ++ encodeList encodeRat x.2.1 ++ encodeRat x.2.2
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List Nat) → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))

def Goal : Prop :=
  ∃ (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List Nat) → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end NonuniformCostUnanimousVote
