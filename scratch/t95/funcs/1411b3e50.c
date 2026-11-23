__int64 __fastcall sub_1411B3E50(__int64 a1, __int64 a2)
{
  __int64 *v4; // r14
  __int64 *v5; // r12
  __int64 v6; // r15
  double v7; // xmm6_8
  double v8; // xmm7_8
  __int64 v9; // rsi
  __int64 v10; // rcx
  __int64 v11; // rax
  __int64 v12; // rbx
  __int64 v13; // rcx
  __int64 v14; // rax
  char *v15; // r15
  __int64 v16; // r15
  __int16 v17; // ax
  int v18; // edi
  int v19; // esi
  __int64 v20; // r8
  __int64 v21; // r8
  __int64 v22; // rax
  __int64 v23; // r9
  int v24; // eax
  double v25; // xmm0_8
  int v26; // eax
  bool v27; // cc
  __int64 v28; // rax
  int v30; // [rsp+40h] [rbp-40h]
  __int64 v31; // [rsp+50h] [rbp-30h]
  __int64 v32; // [rsp+58h] [rbp-28h]
  int v33; // [rsp+60h] [rbp-20h]
  char v34; // [rsp+66h] [rbp-1Ah] BYREF
  char v35; // [rsp+67h] [rbp-19h] BYREF
  __int64 v36; // [rsp+68h] [rbp-18h]

  v36 = -2;
  v34 = 0;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v4 = *(__int64 **)(a1 + 56);
  v5 = *(__int64 **)(a1 + 64);
  if ( v4 == v5 )
    return 0;
  v6 = a2 + 76;
  v7 = MEMORY[0x1417E3628];
  v8 = MEMORY[0x1417EC5F0];
  v31 = 0;
  v33 = 0;
  do
  {
    v9 = *v4;
    v10 = *v4 + *(int *)(*(_QWORD *)(*v4 + 8) + 4LL) + 8;
    v11 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v10 + 1720LL))(v10);
    if ( v11 != 0 )
    {
      v12 = v11;
      if ( (*(_BYTE *)(a1 + 47) != 0
         || (unsigned __int8)sub_1410D43A0(v9, *(_QWORD *)(a1 + 48)) == 0
         && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 664LL))(v9) == 0)
        && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 112LL))(v9) == 0
        && (*(char (__fastcall **)(__int64))(*(_QWORD *)v9 + 808LL))(v9) <= 14 )
      {
        if ( a2 == 0
          || (LOBYTE(v30) = 0,
              (*(unsigned __int8 (__fastcall **)(__int64, __int64, __int64, __int64, _QWORD, char *, _QWORD, _QWORD, int))(*(_QWORD *)v9 + 696LL))(
                v9,
                a1,
                v6,
                a2,
                0,
                &v34,
                0,
                0,
                v30) != 0) )
        {
          if ( (unsigned __int8)sub_140E16740(v12) == 0 )
          {
            v32 = v6;
            v13 = v12 + *(int *)(*(_QWORD *)(v12 + 8) + 4LL) + 8;
            v14 = (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD))(*(_QWORD *)v13 + 1024LL))(
                    v13,
                    *(_QWORD *)(a1 + 48),
                    0);
            if ( v14 == 0
              || (v15 = (char *)v14, (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v14 + 136LL))(v14) == 5)
              || v15[83] >= 60 && (v15[87] < 3 || v15[88] >= 2) )
            {
              v16 = a2;
              v17 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 40LL))(v9);
              v18 = (__int16)(v17 / 50 + (*(__int16 (__fastcall **)(__int64))(*(_QWORD *)v9 + 32LL))(v9) / 50);
              v19 = v18 + 2 * (*(__int16 (__fastcall **)(__int64))(*(_QWORD *)v9 + 8LL))(v9);
              LOBYTE(v20) = 1;
              if ( (*(__int64 (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)qword_141B5EC98 + 536LL))(
                     qword_141B5EC98,
                     v12,
                     v20) != 0 )
              {
                LOBYTE(v21) = 1;
                v22 = (*(__int64 (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)qword_141B5EC98 + 536LL))(
                        qword_141B5EC98,
                        v12,
                        v21);
                LOBYTE(v23) = *(_BYTE *)(a1 + 40) == 0;
                v35 = 0;
                v24 = sub_141461F00(v22 + 116, 0, &v35, v23);
                if ( v35 != 0 )
                  v25 = (double)v24 / v8 / (double)v35;
                else
                  v25 = 0.0;
                a2 = v16;
                v19 += (int)(v25 * v7);
              }
              else
              {
                a2 = v16;
              }
              v6 = v32;
              v26 = v33;
              v27 = v19 <= v33;
              if ( v19 > v33 )
                v26 = v19;
              v33 = v26;
              v28 = v31;
              if ( !v27 )
                v28 = v12;
              v31 = v28;
            }
            else
            {
              v6 = v32;
            }
          }
        }
      }
    }
    ++v4;
  }
  while ( v4 != v5 );
  return v31;
}
