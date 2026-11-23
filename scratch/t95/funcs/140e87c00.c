__int64 __fastcall sub_140E87C00(__int64 a1, int a2, __int64 *a3)
{
  unsigned int v3; // r15d
  __int64 *v4; // rax
  __int64 v5; // rsi
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 *v10; // rdx
  bool v11; // zf
  __int64 **v12; // rcx
  __int64 *v13; // rax
  __int64 *v14; // rcx
  __int64 v15; // rdi
  char v16; // r12
  __int64 v17; // rax
  __int64 v18; // rcx
  __int64 v19; // rdx
  __int64 *v20; // rbx
  __int64 v21; // rbp
  __int64 v22; // r8
  __int64 v23; // rbp
  unsigned int v24; // eax
  unsigned int v25; // eax
  int v26; // eax
  int v27; // eax
  int v28; // edx
  int v29; // eax
  int v30; // eax
  int v31; // edx
  int v32; // eax
  __int64 v34; // rax
  __int64 v35; // rbp
  __int64 v36; // rbp
  __int64 v37; // rbx
  _QWORD *v38; // rdi
  __int64 v39; // rdx
  __int64 v40; // rcx
  int v41; // [rsp+48h] [rbp-50h] BYREF
  __int64 v42[9]; // [rsp+50h] [rbp-48h] BYREF

  v4 = *(__int64 **)(a1 + 24);
  LOBYTE(v3) = 1;
  if ( v4 == *(__int64 **)(a1 + 32) )
    return v3;
  v5 = *v4;
  if ( *v4 == 0 )
    return v3;
  v8 = *v4;
  while ( *(_QWORD *)(v8 + 120) == 0 )
  {
    v9 = *(_QWORD *)(v8 + 48);
    if ( v9 != 0 )
    {
      v10 = *(__int64 **)(v9 + 24);
      if ( *(__int64 **)(v9 + 32) != v10 )
      {
        v11 = *v10 == v8;
        v8 = *v10;
        if ( !v11 )
          continue;
      }
    }
    return v3;
  }
  v12 = *(__int64 ***)(qword_141B5FE30 + 128);
  v13 = *v12;
  v14 = v12[1];
  while ( v13 != v14 )
  {
    v15 = *v13;
    if ( *(_QWORD *)(*v13 + 24) == v5 && (unsigned __int8)(*(_BYTE *)(v15 + 100) - 3) > 2u )
    {
      v16 = 0;
      goto LABEL_22;
    }
    ++v13;
  }
  if ( dword_141B5DFE0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5DFE0);
    if ( dword_141B5DFE0 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5DF90, 1100154003, 16, 112, 0, 0, 16, 4096);
      sub_141751048(sub_140E9C670);
      sub_141750EA0(&dword_141B5DFE0);
    }
  }
  v15 = sub_1407E58C0(&unk_141B5DF90, 112);
  *(_QWORD *)(v15 + 8) = -1;
  *(_DWORD *)(v15 + 16) = 0;
  *(_QWORD *)v15 = 0x1418BD5A8LL;
  *(_QWORD *)(v15 + 48) = 0x76C0001076C0001LL;
  *(_QWORD *)(v15 + 32) = 0;
  *(_QWORD *)(v15 + 40) = 0;
  *(_QWORD *)(v15 + 64) = 0xFFFFFFFFLL;
  *(_QWORD *)(v15 + 72) = 0;
  *(_QWORD *)(v15 + 80) = -1;
  *(_QWORD *)(v15 + 88) = -1;
  *(_QWORD *)(v15 + 56) = -4170448895LL;
  *(_DWORD *)(v15 + 96) = -1;
  *(_DWORD *)(v15 + 102) = -1;
  *(_WORD *)(v15 + 100) = 1;
  *(_QWORD *)(v15 + 24) = v5;
  v17 = v5;
  do
  {
    v18 = *(_QWORD *)(v17 + 120);
    if ( v18 != 0 )
      break;
    v19 = *(_QWORD *)(v17 + 48);
    if ( v19 == 0 )
      break;
    v20 = *(__int64 **)(v19 + 24);
    if ( *(__int64 **)(v19 + 32) == v20 )
      break;
    v11 = *v20 == v17;
    v17 = *v20;
  }
  while ( !v11 );
  *(_QWORD *)(v15 + 32) = v18;
  v16 = 1;
LABEL_22:
  if ( a2 > 1131638125 )
  {
    if ( a2 == 1131638369 )
    {
      v23 = qword_141B5FE28;
      sub_140FE7960((__int64)v42, a3, 0);
      *(_QWORD *)(v15 + 72) = sub_140F7A940(v23, (int *)v42);
    }
    else
    {
      if ( a2 != 1131638126 )
        goto LABEL_37;
      v21 = qword_141B5FE28;
      sub_140FE7960((__int64)v42, a3, 0);
      *(_QWORD *)(v15 + 40) = sub_140F7A940(v21, (int *)v42);
    }
LABEL_60:
    if ( *(_QWORD *)(v15 + 40) == 0
      && *(_QWORD *)(v15 + 32) != 0
      && (*(_WORD *)(v15 + 48) & 0x1FF) == 1
      && *(_WORD *)(v15 + 50) == 1900
      && (*(_WORD *)(v15 + 52) & 0x1FF) == 1
      && *(_WORD *)(v15 + 54) == 1900 )
    {
      if ( v16 != 0 )
      {
        sub_140E98540(v15);
      }
      else
      {
        v34 = qword_141B5FE30;
        v35 = *(_QWORD *)(*(_QWORD *)(qword_141B5FE30 + 128) + 8LL) - **(_QWORD **)(qword_141B5FE30 + 128);
        if ( v35 != 0 )
        {
          v36 = v35 >> 3;
          v37 = (v36 << 32) - 0x100000000LL;
          do
          {
            v38 = *(_QWORD **)(v34 + 128);
            v39 = *(_QWORD *)(*v38 + 8 * v36-- - 8);
            if ( v39 != 0 && *(_QWORD *)(v39 + 24) == v5 )
            {
              v40 = *(_QWORD *)(*v38 + (v37 >> 29));
              if ( v40 != 0 )
                sub_140E98540(v40);
              sub_141758A00();
              v38[1] -= 8LL;
              v34 = qword_141B5FE30;
            }
            v37 -= 0x100000000LL;
          }
          while ( v36 != 0 );
        }
      }
    }
    else if ( v16 != 0 )
    {
      v32 = *(_DWORD *)(qword_141B5FE30 + 80) + 1;
      *(_DWORD *)(v15 + 12) = v32;
      if ( v32 == 0 )
        *(_DWORD *)(v15 + 12) = *(_DWORD *)(qword_141B5FE30 + 80) + 1;
      LOBYTE(v3) = 1;
      LOBYTE(v22) = 1;
      sub_140F6C770(qword_141B5FE30, v15, v22);
    }
    return v3;
  }
  if ( a2 == 1131637348 )
  {
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5C8D0);
      if ( dword_141B5C8D0 == -1 )
      {
        sub_140DBC9B0(&qword_141B5C8A0);
        sub_141751048(sub_140DBCA10);
        sub_141750EA0(&dword_141B5C8D0);
      }
    }
    if ( (__int64 *)*a3 == &qword_141B5C8A0 )
    {
      v25 = *((_DWORD *)a3 + 2);
      HIWORD(v41) = v25 >> 17;
      LOWORD(v41) = (v25 >> 8) & 0x1FF | ((_WORD)v25 << 9);
    }
    else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
    {
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*a3 + 160LL))(*a3, v42, a3);
      sub_1413CA830(&v41, v42);
    }
    else
    {
      v41 = 124518401;
    }
    *(_DWORD *)(v15 + 52) = v41;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0
      && (*(_WORD *)(v15 + 52) & 0x1FF) == 1
      && *(_WORD *)(v15 + 54) == 1900 )
    {
      v29 = (unsigned __int16)word_141AB0260;
      if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
      {
        word_141AB0260 = 2023;
        LOWORD(v29) = 2023;
      }
      v30 = v29 + 1;
      v31 = 3;
      if ( (unsigned __int16)(23593 * v30) < 0xA3Eu )
        v31 = 15;
      *(_DWORD *)(v15 + 52) = ((v31 & v30) == 0) + (v30 << 16) + 182;
    }
    goto LABEL_60;
  }
  if ( a2 == 1131637860 )
  {
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5C8D0);
      if ( dword_141B5C8D0 == -1 )
      {
        sub_140DBC9B0(&qword_141B5C8A0);
        sub_141751048(sub_140DBCA10);
        sub_141750EA0(&dword_141B5C8D0);
      }
    }
    if ( (__int64 *)*a3 == &qword_141B5C8A0 )
    {
      v24 = *((_DWORD *)a3 + 2);
      HIWORD(v41) = v24 >> 17;
      LOWORD(v41) = (v24 >> 8) & 0x1FF | ((_WORD)v24 << 9);
    }
    else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
    {
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*a3 + 160LL))(*a3, v42, a3);
      sub_1413CA830(&v41, v42);
    }
    else
    {
      v41 = 124518401;
    }
    *(_DWORD *)(v15 + 48) = v41;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0
      && (*(_WORD *)(v15 + 48) & 0x1FF) == 1
      && *(_WORD *)(v15 + 50) == 1900 )
    {
      v26 = (unsigned __int16)word_141AB0260;
      if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
      {
        word_141AB0260 = 2023;
        LOWORD(v26) = 2023;
      }
      v27 = v26 + 1;
      v28 = 3;
      if ( (unsigned __int16)(23593 * v27) < 0xA3Eu )
        v28 = 15;
      *(_DWORD *)(v15 + 48) = ((v28 & v27) == 0) + (v27 << 16) + 182;
    }
    goto LABEL_60;
  }
LABEL_37:
  if ( v16 != 0 )
    sub_140E98540(v15);
  return 0;
}
