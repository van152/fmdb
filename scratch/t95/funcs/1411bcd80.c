__int64 __fastcall sub_1411BCD80(__int64 a1, __int64 a2, __int64 a3)
{
  __int64 *v3; // r14
  __int64 result; // rax
  __int64 v5; // r13
  __int64 v6; // rcx
  __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // rcx
  __int64 v10; // rdi
  __int64 v11; // rsi
  __int64 v12; // rdi
  __int64 v13; // rcx
  __int64 v14; // r13
  char v15; // di
  __int64 v16; // rdi
  __int64 v17; // rsi
  unsigned __int64 j; // r15
  __int64 v19; // rax
  unsigned __int64 k; // rcx
  unsigned __int64 v21; // rax
  __int64 v22; // rdi
  __int64 v23; // rdx
  __int64 v24; // rdi
  __int64 v25[3]; // [rsp+38h] [rbp-48h] BYREF
  __int64 v26[2]; // [rsp+50h] [rbp-30h] BYREF
  __int128 v27; // [rsp+60h] [rbp-20h] BYREF
  __int64 v28; // [rsp+70h] [rbp-10h]
  _BYTE v29[40]; // [rsp+78h] [rbp-8h] BYREF
  __int64 i; // [rsp+A0h] [rbp+20h]
  __int64 v31; // [rsp+A8h] [rbp+28h]
  __int64 v32; // [rsp+B0h] [rbp+30h]
  __int64 v33; // [rsp+B8h] [rbp+38h]
  _QWORD v34[2]; // [rsp+C0h] [rbp+40h] BYREF
  __int128 v35; // [rsp+D0h] [rbp+50h] BYREF
  __int128 v36; // [rsp+E0h] [rbp+60h]
  char v37; // [rsp+F0h] [rbp+70h]
  _QWORD v38[2]; // [rsp+100h] [rbp+80h] BYREF
  __int64 v39; // [rsp+110h] [rbp+90h]
  __int64 v40; // [rsp+118h] [rbp+98h] BYREF
  _QWORD v41[2]; // [rsp+120h] [rbp+A0h] BYREF
  char v42; // [rsp+130h] [rbp+B0h]
  __int64 v43; // [rsp+138h] [rbp+B8h]

  v43 = -2;
  v33 = a3;
  v32 = a2;
  v3 = *(__int64 **)(a1 + 56);
  result = *(_QWORD *)(a1 + 64);
  for ( i = result; v3 != (__int64 *)i; ++v3 )
  {
    v5 = *v3;
    v6 = *v3 + *(int *)(*(_QWORD *)(*v3 + 8) + 4LL) + 8;
    result = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v6 + 1312LL))(v6);
    if ( (_BYTE)result == 0 )
    {
      v7 = v5 + *(int *)(*(_QWORD *)(v5 + 8) + 4LL) + 8;
      result = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v7 + 1712LL))(v7);
      if ( result != 0 )
      {
        v10 = result;
        v11 = sub_140FE8230(v9, v8);
        v31 = sub_140FE35F0();
        v12 = v10 + *(int *)(*(_QWORD *)(v10 + 8) + 4LL) + 8;
        *(_OWORD *)v38 = 0;
        v39 = 0;
        sub_1407C9510(&v40);
        v42 = 0;
        (*(void (__fastcall **)(__int64, _QWORD *, _QWORD, __int64, __int64, __int64, _QWORD))(*(_QWORD *)qword_141B5E520
                                                                                             + 56LL))(
          qword_141B5E520,
          v38,
          0,
          v12,
          v31,
          v11,
          0);
        sub_1407C9510(v25);
        v13 = v5 + *(int *)(*(_QWORD *)(v5 + 8) + 4LL) + 8;
        (*(void (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v13 + 144LL))(v13, v34);
        sub_140FEAD00((int *)v34, &v27);
        sub_140835380(v25, 1685218662, (__int64 *)&v27);
        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v34[1] + 16LL))(v34[1], &v34[1]);
        v14 = v33;
        v15 = v42;
        if ( v42 != 0 )
        {
          v36 = 0;
          v35 = 0;
          *(_OWORD *)v34 = 0;
          sub_1408367A0((char *)&v35 + 8, (v41[0] - v40) >> 4, &v40, v41);
          v37 = v15;
          sub_1415D1990(v34);
          sub_1415D1320(v34, &v27);
          sub_140835380(v25, 1349740140, (__int64 *)&v27);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
          v16 = v32 + 24LL * v42;
          sub_14083DC80(&v27, v25);
          sub_14083B5F0(v16, &v27);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
          sub_140833970((char *)&v35 + 8);
          v14 = v33;
        }
        v36 = 0;
        v35 = 0;
        *(_OWORD *)v34 = 0;
        sub_1408367A0((char *)&v35 + 8, (qword_141B5A460 - qword_141B5A458) >> 4, &qword_141B5A458, &qword_141B5A460);
        v37 = 0;
        v42 = 0;
        while ( (unsigned __int8)sub_1415D15F0(v38, v34, 0) != 0 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *, _QWORD, _QWORD, _QWORD, __int128 *, _QWORD))(*(_QWORD *)qword_141B5E520 + 32LL))(
                 qword_141B5E520,
                 v34,
                 0,
                 0,
                 0,
                 &v27,
                 0) != 0 )
          {
            v28 = v35;
            v27 = *(_OWORD *)v34;
            memset(v29, 0, 24);
            sub_1408367A0(v29, (v41[0] - v40) >> 4, &v40, v41);
            v29[24] = 0;
            sub_1415D1990(&v27);
            sub_1415D1320(&v27, v26);
            sub_140835380(v25, 1349740140, v26);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v26[0] + 16LL))(v26[0], v26);
            v17 = v14;
            for ( j = 0; j != 164; ++j )
            {
              if ( (unsigned __int8)sub_1415EA960((unsigned int)j) == 0 )
              {
                v19 = v34[j >> 6];
                if ( _bittest64(&v19, j) )
                {
                  sub_14083DC80(v26, v25);
                  sub_14083B5F0(v17, v26);
                  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v26[0] + 16LL))(v26[0], v26);
                }
              }
              v17 += 24;
            }
            sub_140833970(v29);
          }
          if ( v37 == v42 )
            v42 = 0;
          for ( k = 0; k != 164; ++k )
          {
            v21 = k >> 6;
            v22 = v34[k >> 6];
            v23 = 1LL << k;
            if ( _bittest64(&v22, k) )
            {
              v24 = v38[v21];
              if ( (v23 & v24) != 0 )
                v38[v21] = ~v23 & v24;
            }
          }
        }
        sub_140833970((char *)&v35 + 8);
        sub_140833970(v25);
        result = sub_140833970(&v40);
      }
    }
  }
  return result;
}
