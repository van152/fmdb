char __fastcall sub_140E97410(__int64 a1, int a2, __int64 *a3)
{
  __int64 *v6; // rsi
  char result; // al
  __int64 **v8; // rdx
  __int64 *v9; // rcx
  __int64 *v10; // rdx
  __int64 v11; // rsi
  __int64 v12; // rdi
  __int64 *v13; // rcx
  __int64 *v14; // rax
  __int64 v15; // rcx
  __int64 v16; // rax
  int v17; // esi
  __int64 v18; // rax
  __int64 *v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rax
  int v22; // esi
  __int64 *v23; // rax
  __int64 v24; // rcx
  __int64 *v25; // rax
  __int64 v26; // rcx
  __int64 *v27; // [rsp+28h] [rbp-18h] BYREF
  __int64 v28; // [rsp+30h] [rbp-10h]
  __int64 v29; // [rsp+38h] [rbp-8h]

  v29 = -2;
  if ( a3 != &qword_141B5A4A0 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
      qword_141B5A4A0,
      &qword_141B5A4A0,
      a3);
  }
  v6 = *(__int64 **)(a1 + 24);
  result = 1;
  if ( *(__int64 **)(a1 + 32) == v6 )
    return 1;
  v8 = *(__int64 ***)(qword_141B5FE30 + 128);
  v9 = *v8;
  v10 = v8[1];
  if ( v9 == v10 )
    return 1;
  v11 = *v6;
  while ( 1 )
  {
    v12 = *v9;
    if ( *(_QWORD *)(*v9 + 24) == v11 && (unsigned __int8)(*(_BYTE *)(v12 + 100) - 3) > 2u )
      break;
    if ( ++v9 == v10 )
      return result;
  }
  result = 0;
  if ( a2 <= 1131638125 )
  {
    if ( a2 == 1131637348 )
    {
      if ( (*(_WORD *)(v12 + 52) & 0x1FF) != 1 || *(_WORD *)(v12 + 54) != 1900 )
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
        LODWORD(v28) = ((*(_WORD *)(v12 + 52) & 0x1FF) << 8)
                     | (*(unsigned __int16 *)(v12 + 52) >> 9)
                     | (*(unsigned __int16 *)(v12 + 54) << 17);
        v13 = &qword_141B5C8A0;
        v27 = &qword_141B5C8A0;
        if ( &v27 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v25 = v27;
          v26 = v28;
          a3[1] = v28;
          *a3 = (__int64)v25;
          v13 = (__int64 *)(sub_14083D4F0(v26) + 8);
          v28 = 0;
          v27 = v13;
        }
        goto LABEL_35;
      }
    }
    else
    {
      if ( a2 != 1131637860 )
        return result;
      if ( (*(_WORD *)(v12 + 48) & 0x1FF) != 1 || *(_WORD *)(v12 + 50) != 1900 )
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
        LODWORD(v28) = ((*(_WORD *)(v12 + 48) & 0x1FF) << 8)
                     | (*(unsigned __int16 *)(v12 + 48) >> 9)
                     | (*(unsigned __int16 *)(v12 + 50) << 17);
        v13 = &qword_141B5C8A0;
        v27 = &qword_141B5C8A0;
        if ( &v27 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v14 = v27;
          v15 = v28;
          a3[1] = v28;
          *a3 = (__int64)v14;
          v13 = (__int64 *)(sub_14083D4F0(v15) + 8);
          v28 = 0;
          v27 = v13;
        }
LABEL_35:
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v13 + 16))(v13, &v27);
        return 1;
      }
    }
    if ( a3 != &qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    return 1;
  }
  if ( a2 == 1131638369 )
  {
    v21 = *(_QWORD *)(v12 + 72);
    if ( v21 == 0 )
      return 1;
    v22 = *(_DWORD *)(v21 + 12);
    v18 = sub_14083D4F0(v9) + 40;
    LODWORD(v28) = v22;
    v27 = (__int64 *)v18;
    if ( &v27 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v23 = v27;
      v24 = v28;
      a3[1] = v28;
      *a3 = (__int64)v23;
      v18 = sub_14083D4F0(v24) + 8;
      v28 = 0;
      v27 = (__int64 *)v18;
    }
    goto LABEL_23;
  }
  if ( a2 != 1131638126 )
    return result;
  v16 = *(_QWORD *)(v12 + 40);
  if ( v16 != 0 )
  {
    v17 = *(_DWORD *)(v16 + 12);
    v18 = sub_14083D4F0(v9) + 40;
    LODWORD(v28) = v17;
    v27 = (__int64 *)v18;
    if ( &v27 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v19 = v27;
      v20 = v28;
      a3[1] = v28;
      *a3 = (__int64)v19;
      v18 = sub_14083D4F0(v20) + 8;
      v28 = 0;
      v27 = (__int64 *)v18;
    }
LABEL_23:
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v18 + 16LL))(v18, &v27);
  }
  return 1;
}
