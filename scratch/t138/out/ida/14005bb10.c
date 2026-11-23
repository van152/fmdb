bool sub_14005BB10()
{
  __int64 v0; // r15
  __int64 v1; // rsi
  __int64 v2; // rcx
  __int64 v3; // rsi
  __int64 v4; // rdi
  __int64 v5; // rsi
  __int64 v6; // rdi
  __int64 v7; // rbx
  __int64 v8; // rdi
  __int64 v9; // rsi
  __int64 v10; // rbx
  __int64 v11; // rsi
  __int64 v12; // rdi
  __int64 v13; // rbx
  __int64 v14; // rdi
  __int64 v15; // rsi
  unsigned __int64 v16; // rax
  unsigned __int64 v17; // r13
  unsigned __int64 v18; // rdx
  __int64 v19; // r14
  __int64 v20; // rbx
  __int64 v21; // rbp
  __int64 v22; // r9
  __int64 v23; // rax
  __int64 v24; // r14
  __int64 v25; // rsi
  unsigned __int64 v26; // rax
  unsigned __int64 v27; // r13
  unsigned __int64 v28; // rdx
  __int64 v29; // rdi
  __int64 v30; // rbx
  __int64 v31; // rbp
  __int64 v32; // rsi
  void (__fastcall ***v33)(_QWORD, __int64); // rcx
  int v35; // [rsp+20h] [rbp-88h]
  __int128 v36; // [rsp+30h] [rbp-78h] BYREF
  __int64 v37; // [rsp+40h] [rbp-68h]
  __int64 v38; // [rsp+48h] [rbp-60h] BYREF
  __int64 v39; // [rsp+50h] [rbp-58h] BYREF
  __int64 v40; // [rsp+58h] [rbp-50h] BYREF
  _BYTE v41[72]; // [rsp+60h] [rbp-48h] BYREF

  sub_140E480B0(a1: &v38);
  v0 = v38;
  if ( v38 != 0 )
  {
    v1 = qword_141ABF5C0;
    sub_1407D8AB0(a1: &v36, a2: 0x1418E2C24LL);
    v39 = 0;
    sub_140809040(a1: &v39, a2: 0x1418D9738LL, a3: 0xFFFFFFFFLL);
    sub_1407D5F40(a1: v41, a2: &v39);
    sub_1400015E0(a1: v1, a2: &v38, a3: v41, a4: &v36, a5: 1);
    sub_140808B00(a1: v41);
    sub_140808B00(a1: &v39);
    v2 = qword_141ABD470;
    if ( qword_141ABD470 == 0 )
    {
      v2 = sub_1407E4940();
      qword_141ABD470 = v2;
    }
    v36 = 0;
    v37 = 0;
    v3 = sub_1407E4490(a1: v2, a2: 3);
    *(_WORD *)v3 = 58;
    *(_BYTE *)(v3 + 2) = 1;
    v4 = *((_QWORD *)&v36 + 1);
    sub_141758A00(a1: v3, a2: v36, a3: -(__int64)v36);
    if ( v4 != 0 )
      sub_1417589F0(a1: v3 + 3, a2: 0, a3: *((_QWORD *)&v36 + 1));
    if ( (_QWORD)v36 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    *(_QWORD *)&v36 = v3;
    v5 = v3 + 3;
    *((_QWORD *)&v36 + 1) = v5;
    v37 = v5;
    v6 = sub_1407E4490(a1: qword_141ABD470, a2: 6);
    *(_WORD *)(v6 + 3) = 53;
    *(_BYTE *)(v6 + 5) = 1;
    v7 = *((_QWORD *)&v36 + 1);
    sub_141758A00(a1: v6, a2: v36, a3: v5 - v36);
    if ( v7 != v5 )
      sub_141758A00(a1: v6 + 6, a2: v5, a3: *((_QWORD *)&v36 + 1) - v5);
    if ( (_QWORD)v36 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    *(_QWORD *)&v36 = v6;
    v8 = v6 + 6;
    *((_QWORD *)&v36 + 1) = v8;
    v37 = v8;
    v9 = sub_1407E4490(a1: qword_141ABD470, a2: 9);
    *(_WORD *)(v9 + 6) = 827;
    *(_BYTE *)(v9 + 8) = 1;
    v10 = *((_QWORD *)&v36 + 1);
    sub_141758A00(a1: v9, a2: v36, a3: v8 - v36);
    if ( v10 != v8 )
      sub_141758A00(a1: v9 + 9, a2: v8, a3: *((_QWORD *)&v36 + 1) - v8);
    if ( (_QWORD)v36 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    *(_QWORD *)&v36 = v9;
    v11 = v9 + 9;
    *((_QWORD *)&v36 + 1) = v11;
    v37 = v11;
    v12 = sub_1407E4490(a1: qword_141ABD470, a2: 12);
    *(_WORD *)(v12 + 9) = 318;
    *(_BYTE *)(v12 + 11) = 1;
    v13 = *((_QWORD *)&v36 + 1);
    sub_141758A00(a1: v12, a2: v36, a3: v11 - v36);
    if ( v13 != v11 )
      sub_141758A00(a1: v12 + 12, a2: v11, a3: *((_QWORD *)&v36 + 1) - v11);
    if ( (_QWORD)v36 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    *(_QWORD *)&v36 = v12;
    *((_QWORD *)&v36 + 1) = v12 + 12;
    v14 = v12 + 12;
    v37 = v14;
    v15 = v14 - v36;
    v16 = 0xAAAAAAAAAAAAAAABuLL * (v14 - v36);
    v17 = v16 + 1;
    v18 = v16 + (v16 >> 1);
    if ( v18 <= v16 + 1 )
      v18 = v16 + 1;
    if ( v16 > 0x5555555555555555LL - (v16 >> 1) )
      v18 = 0x5555555555555555LL;
    v19 = 3 * v18;
    v20 = sub_1407E4490(a1: qword_141ABD470, a2: 3 * v18);
    *(_WORD *)(v20 + v15) = 576;
    *(_BYTE *)(v20 + v15 + 2) = 1;
    v21 = *((_QWORD *)&v36 + 1);
    sub_141758A00(a1: v20, a2: v36, a3: v14 - v36);
    if ( v21 != v14 )
      sub_141758A00(a1: v20 + v15 + 3, a2: v14, a3: *((_QWORD *)&v36 + 1) - v14);
    if ( (_QWORD)v36 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    *(_QWORD *)&v36 = v20;
    v23 = v20 + 3 * v17;
    *((_QWORD *)&v36 + 1) = v23;
    v24 = v20 + v19;
    v37 = v24;
    if ( v23 == v24 )
    {
      v25 = v24 - v36;
      v26 = 0xAAAAAAAAAAAAAAABuLL * (v24 - v36);
      v27 = v26 + 1;
      v28 = v26 + (v26 >> 1);
      if ( v28 <= v26 + 1 )
        v28 = v26 + 1;
      if ( v26 > 0x5555555555555555LL - (v26 >> 1) )
        v28 = 0x5555555555555555LL;
      v29 = 3 * v28;
      v30 = sub_1407E4490(a1: qword_141ABD470, a2: 3 * v28);
      *(_WORD *)(v30 + v25) = 34;
      *(_BYTE *)(v30 + v25 + 2) = 0;
      v31 = *((_QWORD *)&v36 + 1);
      sub_141758A00(a1: v30, a2: v36, a3: v24 - v36);
      if ( v31 != v24 )
        sub_141758A00(a1: v30 + v25 + 3, a2: v24, a3: *((_QWORD *)&v36 + 1) - v24);
      if ( (_QWORD)v36 != 0 )
        sub_1407E4890(a1: qword_141ABD470);
      *(_QWORD *)&v36 = v30;
      *((_QWORD *)&v36 + 1) = v30 + 3 * v27;
      v37 = v30 + v29;
    }
    else
    {
      *(_WORD *)v23 = 34;
      *(_BYTE *)(v23 + 2) = 0;
      *((_QWORD *)&v36 + 1) += 3LL;
    }
    LOWORD(v22) = 45;
    sub_140E481A0(a1: &v36, a2: 0, a3: 0x7FFFFFFF, a4: v22);
    v32 = qword_141ABF5C0;
    sub_1407D8AB0(a1: v41, a2: 0x1418E2C24LL);
    v40 = 0;
    sub_140809040(a1: &v40, a2: 0x1418D9738LL, a3: 0xFFFFFFFFLL);
    sub_1407D5F40(a1: &v39, a2: &v40);
    sub_1400015E0(a1: v32, a2: &v38, a3: &v39, a4: v41, a5: v35);
    sub_140808B00(a1: &v39);
    sub_140808B00(a1: &v40);
    if ( (_QWORD)v36 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    v33 = (void (__fastcall ***)(_QWORD, __int64))v38;
    if ( v38 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 8)) == 0 )
      (**v33)(a1: v33, a2: 1);
  }
  return v0 != 0;
}
