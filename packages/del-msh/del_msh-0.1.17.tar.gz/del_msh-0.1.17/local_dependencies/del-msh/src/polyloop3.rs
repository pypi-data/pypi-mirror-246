//! methods for 3D poly loop

use num_traits::AsPrimitive;

fn match_frames_of_two_ends<T>(
    vtx2xyz: &[T],
    vtx2bin0: &nalgebra::Matrix3xX::<T>) -> nalgebra::Matrix3xX::<T>
    where T: nalgebra::RealField + Copy + 'static,
          f64: AsPrimitive<T>,
          usize: AsPrimitive<T>
{
    use del_geo::vec3::navec3;
    let num_vtx = vtx2xyz.len() / 3;
    let theta = {
        let x0 = vtx2bin0.column(0);
        let xn = vtx2bin0.column(num_vtx - 1);
        let vn0 = (navec3(vtx2xyz, 0) - navec3(vtx2xyz, num_vtx - 1)).normalize();
        let v01 = (navec3(vtx2xyz, 1) - navec3(vtx2xyz, 0)).normalize();
        assert!(x0.dot(&v01).abs() < 1.0e-6_f64.as_());
        let rot = del_geo::mat3::minimum_rotation_matrix(vn0, v01);
        let x1a = rot * xn;
        let y0 = v01.cross(&x0);
        assert!(x1a.dot(&v01).abs() < 1.0e-6_f64.as_());
        assert!((y0.norm() - 1.0_f64.as_()).abs() < 1.0e-6_f64.as_());
        let c0 = x1a.dot(&x0);
        let s0 = x1a.dot(&y0);
        T::atan2(s0, c0)
    };
    let theta_step = theta / num_vtx.as_();
    let mut vtx2bin1 = nalgebra::Matrix3xX::<T>::zeros(num_vtx);
    for iseg in 0..num_vtx {
        let dtheta = theta_step * iseg.as_();
        let x0 = vtx2bin0.column(iseg);
        let ivtx0 = iseg;
        let ivtx1 = (iseg + 1) % num_vtx;
        let v01 = (navec3(vtx2xyz, ivtx1) - navec3(vtx2xyz, ivtx0)).normalize();
        let y0 = v01.cross(&x0);
        assert!((x0.cross(&y0).dot(&v01) - 1.as_()).abs() < 1.0e-5_f64.as_());
        let x1 = x0.scale(dtheta.sin()) + y0.scale(dtheta.cos());
        vtx2bin1.column_mut(iseg).copy_from(&x1);
    }
    vtx2bin1
}

pub fn smooth_frame<T>(
    vtx2xyz: &[T]) -> nalgebra::Matrix3xX::<T>
    where T: nalgebra::RealField + 'static + Copy,
          f64: num_traits::AsPrimitive<T>,
          usize: num_traits::AsPrimitive<T>
{
    let vtx2bin0 = crate::polyline::parallel_transport_polyline(vtx2xyz);
    match_frames_of_two_ends(vtx2xyz, &vtx2bin0)
}

pub fn tube_mesh(
    vtx2xyz: &nalgebra::Matrix3xX::<f32>,
    vtx2bin: &nalgebra::Matrix3xX::<f32>,
    rad: f32) -> (Vec<usize>, Vec<f32>) {
    let n = 8;
    let dtheta = std::f32::consts::PI * 2. / n as f32;
    let num_vtx = vtx2xyz.ncols();
    let mut pnt2xyz = Vec::<f32>::new();
    for ipnt in 0..num_vtx {
        let p0 = vtx2xyz.column(ipnt).into_owned();
        let p1 = vtx2xyz.column((ipnt + 1) % num_vtx).into_owned();
        let z0 = (p1 - p0).normalize();
        let x0 = vtx2bin.column(ipnt);
        let y0 = z0.cross(&x0);
        for i in 0..n {
            let theta = dtheta * i as f32;
            let v0 = x0.scale(theta.cos()) + y0.scale(theta.sin());
            let q0 = p0 + v0.scale(rad);
            q0.iter().for_each(|&v| pnt2xyz.push(v));
        }
    }

    let mut tri2pnt = Vec::<usize>::new();
    for iseg in 0..num_vtx {
        let ipnt0 = iseg;
        let ipnt1 = (ipnt0 + 1) % num_vtx;
        for i in 0..n {
            tri2pnt.push(ipnt0 * n + i);
            tri2pnt.push(ipnt0 * n + (i + 1) % n);
            tri2pnt.push(ipnt1 * n + i);
            //
            tri2pnt.push(ipnt1 * n + (i + 1) % n);
            tri2pnt.push(ipnt1 * n + i);
            tri2pnt.push(ipnt0 * n + (i + 1) % n);
        }
    }
    (tri2pnt, pnt2xyz)
}

pub fn smooth_gradient_of_distance(
    vtx2xyz: &[f64],
    q: &nalgebra::Vector3::<f64>) -> nalgebra::Vector3::<f64>
{
    use del_geo::vec3::navec3;
    let n = vtx2xyz.len() / 3;
    let mut dd = nalgebra::Vector3::<f64>::zeros();
    for iseg in 0..n {
        let ip0 = iseg;
        let ip1 = (iseg + 1) % n;
        let (_, dd0) = del_geo::edge3::wdw_integral_of_inverse_distance_cubic(
            q,
            &navec3(vtx2xyz, ip0),
            &navec3(vtx2xyz, ip1));
        dd += dd0;
    }
    dd
}

pub fn extend_avoid_intersection(
    p0: &nalgebra::Vector3::<f64>,
    v0: &nalgebra::Vector3::<f64>,
    vtx2xyz: &[f64],
    eps: f64,
    n: usize) -> nalgebra::Vector3::<f64>
{
    let mut p1 = p0 + v0.scale(eps);
    for _i in 0..n {
        let v1 = -smooth_gradient_of_distance(vtx2xyz, &p1).normalize();
        p1 += v1.scale(eps);
    }
    p1
}

pub fn tube_mesh_avoid_intersection(
    vtx2xyz: &[f64],
    vtx2bin: &nalgebra::Matrix3xX::<f64>,
    eps: f64,
    niter: usize) -> (Vec<usize>, Vec<f64>)
{
    use del_geo::vec3::navec3;
    let n = 8;
    let dtheta = std::f64::consts::PI * 2. / n as f64;
    let num_vtx = vtx2xyz.len() / 3;
    let mut pnt2xyz = Vec::<f64>::new();
    for ipnt in 0..num_vtx {
        let p0 = navec3(vtx2xyz, ipnt);
        let p1 = navec3(vtx2xyz, (ipnt + 1) % num_vtx);
        let z0 = (p1 - p0).normalize();
        let x0 = vtx2bin.column(ipnt);
        let y0 = z0.cross(&x0);
        for i in 0..n {
            let theta = dtheta * i as f64;
            let v0 = x0.scale(theta.cos()) + y0.scale(theta.sin());
            let q0 = extend_avoid_intersection(&p0, &v0, vtx2xyz, eps, niter);
            // let q0 = p0 + v0.scale(rad);
            q0.iter().for_each(|&v| pnt2xyz.push(v));
        }
    }

    let mut tri2pnt = Vec::<usize>::new();
    for iseg in 0..num_vtx {
        let ipnt0 = iseg;
        let ipnt1 = (ipnt0 + 1) % num_vtx;
        for i in 0..n {
            tri2pnt.push(ipnt0 * n + i);
            tri2pnt.push(ipnt0 * n + (i + 1) % n);
            tri2pnt.push(ipnt1 * n + i);
            //
            tri2pnt.push(ipnt1 * n + (i + 1) % n);
            tri2pnt.push(ipnt1 * n + i);
            tri2pnt.push(ipnt0 * n + (i + 1) % n);
        }
    }
    (tri2pnt, pnt2xyz)
}

pub fn write_wavefrontobj<P: AsRef<std::path::Path>>(
    filepath: P,
    vtx2xyz: &nalgebra::Matrix3xX::<f32>) {
    use std::io::Write;
    let mut file = std::fs::File::create(filepath).expect("file not found.");
    for vtx in vtx2xyz.column_iter() {
        writeln!(file, "v {} {} {}",
                 vtx[0], vtx[1], vtx[2]).expect("fail");
    }
    write!(file, "l ").expect("fail");
    for i in 1..vtx2xyz.ncols() + 1 {
        write!(file, "{} ", i).expect("fail");
    }
    writeln!(file, "1").expect("fail");
}

pub fn distance_from_edge3(
    vtx2xyz: &[f64],
    p0: &[f64],
    p1: &[f64]) -> f64{
    assert_eq!(p0.len(),3);
    assert_eq!(p1.len(),3);
    let num_vtx = vtx2xyz.len() / 3;
    assert_eq!(vtx2xyz.len(), num_vtx*3);
    let p0 = nalgebra::Vector3::<f64>::from_row_slice(p0);
    let p1 = nalgebra::Vector3::<f64>::from_row_slice(p1);
    let mut min_dist = f64::MAX;
    for i_edge in 0..num_vtx {
        let iv0 = i_edge;
        let iv1 = (i_edge + 1) % num_vtx;
        let q0 = nalgebra::Vector3::<f64>::from_row_slice(&vtx2xyz[iv0 * 3..iv0 * 3 + 3]);
        let q1 = nalgebra::Vector3::<f64>::from_row_slice(&vtx2xyz[iv1 * 3..iv1 * 3 + 3]);
        let (dist,_,_) = del_geo::edge3::nearest_to_edge3(&p0, &p1, &q0, &q1);
        min_dist = if dist < min_dist {dist} else {min_dist};
    }
    min_dist
}


pub fn winding_number(
    vtx2xyz: &[f64],
    org: &[f64],
    dir: &[f64]) -> f64
{
    use num_traits::FloatConst;
    let org = nalgebra::Vector3::<f64>::from_row_slice(org);
    let dir = nalgebra::Vector3::<f64>::from_row_slice(dir);
    let num_vtx = vtx2xyz.len() / 3;
    assert_eq!(vtx2xyz.len(), num_vtx*3);
    let mut sum = 0.;
    for i_edge in 0..num_vtx {
        let iv0 = i_edge;
        let iv1 = (i_edge + 1) % num_vtx;
        let q0 = nalgebra::Vector3::<f64>::from_row_slice(&vtx2xyz[iv0 * 3..(iv0+1) * 3])-org;
        let q1 = nalgebra::Vector3::<f64>::from_row_slice(&vtx2xyz[iv1 * 3..(iv1+1) * 3])-org;
        let q0 = q0 - dir.scale(q0.dot(&dir));
        let q1 = q1 - dir.scale(q1.dot(&dir));
        let q0 = q0.normalize();
        let q1 = q1.normalize();
        let s = q0.cross(&q1).dot(&dir);
        let c = q0.dot(&q1);
        sum += s.atan2(c);
    }
    sum * f64::FRAC_1_PI() * 0.5
}