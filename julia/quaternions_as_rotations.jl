#!/usr/bin/env julia

import LinearAlgebra: norm
import Rotations: AngleAxis, RotX, RotY, RotZ, Rotation, UnitQuaternion
import StaticArrays: SVector, norm
import Test: @test, @testset

# ---------------------------------------- 
# Note on computational cost of rotations.
# (See, e.g., https://fgiesen.wordpress.com/2019/02/09/rotating-a-single-vector-using-a-quaternion/)
#   * 2 cross products (@ 6 mult + 3 add (add/sub))
#   * 1 3D dot product (@ 3 mult + 2 add)
#   * 3 vector-scalar products (@ 3 mult)
#   * 2 scalar multiplies (for q_r^2 and 2q_r)
#   * 3 vector additions (@ 3 add)
#   * TOTAL: 26 mults + 17 adds
#   * On GPUs: 9 scalar mults + 17 scalar mult-adds
# BUT, by using the unit-length of the quaternion, this can be reduced to
#   * 18 mults + 12 adds, or 15 mults + 15 adds.
#   * On GPUs: 3 mults + 12 mult-adds.
#   * Compare: 3x3 matrices take 9 mults + 6 adds, or 3 mults + 6 mult-adds.
# ---------------------------------------- 
macro assert(bool_expr)
    message = string("Assertion: ", bool_expr, " failed")
    return :($(esc(bool_expr)) || error($message))
end
# ---------------------------------------- 
# ---------------------------------------- 
 
function is_approx(v1::AbstractVector{T}, v2::AbstractVector{T}, eps=10e-10) where T
    length(v1) == length(v2) || error("length mismatch")
    return norm(v1 - v2) < eps
end

function is_approx(rot1, rot2)
    vx = SVector{3,Float64}(1.0, 0.0, 0.0)
    vy = SVector{3,Float64}(0.0, 1.0, 0.0)
    vz = SVector{3,Float64}(0.0, 0.0, 1.0)

    all([ rot1 * vx == rot2 * vx
        , rot1 * vy == rot2 * vy
        , rot1 * vz == rot2 * vz
        ])
end

function is_approx(q1::UnitQuaternion, q2::UnitQuaternion, eps=10e-10) where T
    return norm(q1 - q2) < eps
end
# ---------------------------------------- 

function test_quats(ux, uy, uz)
    q1 = UnitQuaternion(1.0, 0.0, 0.0, 0.0)
    qi = UnitQuaternion(0.0, ux...)
    qj = UnitQuaternion(0.0, uy...)
    qk = UnitQuaternion(0.0, uz...)

    @assert is_approx(qi * qj, qk)
    @assert is_approx(qj * qk, qi)
    @assert is_approx(qk * qi, qj)

    @assert is_approx(qj * qi, -qk)
    @assert is_approx(qk * qj, -qi)
    @assert is_approx(qi * qk, -qj)

    @assert is_approx(qi * qi, -q1)
    @assert is_approx(qj * qj, -q1)
    @assert is_approx(qk * qk, -q1)
end

function test_angleaxis(vx, vy, vz, rx90, ry90, rz90)
    @assert is_approx(rx90 * vx, vx)
    @assert is_approx(ry90 * vy, vy)
    @assert is_approx(rz90 * vz, vz)
    
    @assert is_approx(rx90 * vy, vz)
    @assert is_approx(rx90 * vz, -vy)
    
    @assert is_approx(ry90 * vx, -vz)
    @assert is_approx(ry90 * vz, vx)
    
    @assert is_approx(rz90 * vx, vy)
    @assert is_approx(rz90 * vy, -vx)
end

function test_rotaxis(rx90, ry90, rz90)
    @assert is_approx(rx90, RotX(pi/2))
    @assert is_approx(ry90, RotY(pi/2))
    @assert is_approx(rz90, RotZ(pi/2))
end
# ---------------------------------------- 
@testset "QuaternionsAsRotations" begin
    ux = (1.0, 0.0, 0.0)
    uy = (0.0, 1.0, 0.0)
    uz = (0.0, 0.0, 1.0)

    vx = SVector{3,Float64}(ux...)
    vy = SVector{3,Float64}(uy...)
    vz = SVector{3,Float64}(uz...)

    rx90 = AngleAxis{Float64}(pi/2, ux...)
    ry90 = AngleAxis{Float64}(pi/2, uy...)
    rz90 = AngleAxis{Float64}(pi/2, uz...)
 
    @test test_quats(ux, uy, uz)
    @test test_angleaxis(vx, vy, vz, rx90, ry90, rz90)
    @test test_rotaxis(rx90, ry90, rz90)
end
