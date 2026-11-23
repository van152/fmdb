__int64 __fastcall sub_140F83A50(_QWORD *a1, _QWORD *a2)
{
  _QWORD *v2; // rdi
  _DWORD *v4; // rbx
  __int64 v5; // rbx
  _DWORD *v6; // rbx
  int v7; // eax
  _QWORD *v8; // rdx
  __int64 v9; // r8
  unsigned __int8 v10; // al
  __int64 v11; // rbx
  __int64 v12; // rbx
  unsigned int v13; // ebx
  _QWORD *v14; // rcx
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v17; // rax
  __int64 v18; // r8
  __int64 v19; // rbx
  __int64 v20; // r9
  _QWORD *v21; // rdx
  __int64 v22; // rax
  unsigned __int8 v24; // [rsp+2Bh] [rbp-3Dh] BYREF
  int v25; // [rsp+2Ch] [rbp-3Ch] BYREF
  int v26; // [rsp+30h] [rbp-38h] BYREF
  int v27; // [rsp+34h] [rbp-34h] BYREF
  _BYTE v28[48]; // [rsp+38h] [rbp-30h] BYREF

  v2 = a2;
  v4 = (_DWORD *)*a2;
  if ( (*(_BYTE *)(*a2 + 12LL) & 2) != 0 && HIWORD(qword_141B6034C) != 0 )
  {
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
      v9 = 4;
    else
      v9 = 8;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v4 + 40LL))(*a2, a1, v9);
    if ( v4[4] != 0 )
      goto LABEL_39;
    goto LABEL_20;
  }
  *a1 = 0;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v25, 4);
  if ( *(_DWORD *)(v5 + 16) != 0 )
  {
    *a1 = 0;
LABEL_39:
    LODWORD(v2) = 0;
    return (unsigned int)v2;
  }
  if ( v25 == -1 )
  {
    *a1 = 0;
LABEL_20:
    LOBYTE(v2) = 1;
    return (unsigned int)v2;
  }
  v6 = (_DWORD *)*v2;
  v7 = *(_DWORD *)(*v2 + 12LL);
  if ( (v7 & 2) == 0 )
  {
    (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)v6 + 40LL))(*v2, &v24, 1);
    if ( v6[4] != 0 )
      goto LABEL_39;
    if ( v24 == 0 )
      goto LABEL_9;
LABEL_24:
    v26 = 0;
    v11 = *v2;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v2 + 40LL))(*v2, &v27, 4);
    if ( *(_DWORD *)(v11 + 16) != 0 )
      goto LABEL_39;
    v12 = *v2;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v2 + 40LL))(*v2, &v26, 4);
    if ( *(_DWORD *)(v12 + 16) != 0 )
      goto LABEL_39;
    v13 = 8;
    if ( v24 >= 4u )
      v13 = 255;
    if ( dword_141B5E7A0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5E7A0);
      if ( dword_141B5E7A0 == -1 )
      {
        qword_141B5E770 = 0;
        qword_141B5E768 = 0;
        qword_141B5E760 = 0;
        qword_141B5E758 = 0;
        qword_141B5E778 = -1;
        dword_141B5E780 = -1;
        qword_141B5E788 = 0;
        qword_141B5E790 = 0xFFFFFFFF00000000uLL;
        qword_141B5E798 = 0xFF00000000LL;
        sub_141751048(sub_140F85560);
        sub_141750EA0(&dword_141B5E7A0);
      }
    }
    if ( (unsigned __int8)sub_14132D9A0(&qword_141B5E758, v2, v13) == 0 )
      goto LABEL_39;
    sub_141457510(v28);
    if ( (unsigned __int8)sub_141457830(v28, v2) != 0 )
    {
      if ( (_BYTE)word_141B60320 == 0 )
      {
        LODWORD(v2) = v25;
        v14 = *(_QWORD **)(qword_141B5FE10 + 128);
        if ( (__int64)(v14[1] - *v14) >> 3 > (unsigned __int64)v25
          && (v15 = *(_QWORD *)(*v14 + 8LL * v25), *a1 = v15, v15 != 0) )
        {
          v16 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v15 + 512LL))(v15);
          sub_140F6EBC0(&qword_141B5E758, v16);
          v17 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*a1 + 512LL))(*a1);
          LOBYTE(v18) = 1;
          sub_14157BCF0(v17, v28, v18);
          *(_DWORD *)(*a1 + 12LL) = v27;
        }
        else
        {
          v19 = sub_141750CC0(88);
          sub_14157BBA0(v19, (unsigned int)v2, &qword_141B5E758, v28);
          *(_DWORD *)(v19 + 12) = v27;
          *(_DWORD *)(v19 + 16) = v26;
          LOBYTE(v20) = 1;
          sub_140F6A2E0(qword_141B5FE10, v19, (unsigned int)v25, v20);
        }
      }
      v21 = *(_QWORD **)(qword_141B5FE10 + 128);
      if ( v25 < (int)((v21[1] - *v21) >> 3) )
      {
        v22 = *(_QWORD *)(*v21 + 8LL * v25);
        *a1 = v22;
        LOBYTE(v2) = v22 != 0;
        sub_1414575F0(v28);
        goto LABEL_12;
      }
    }
    sub_1414575F0(v28);
    goto LABEL_39;
  }
  v10 = (2 * ~(_BYTE)v7) & 4;
  if ( byte_141AAE088 == 0 )
    v10 = 0;
  v24 = v10;
  if ( v10 != 0 )
    goto LABEL_24;
LABEL_9:
  LOBYTE(v2) = 1;
  if ( v25 >= 0 )
  {
    v8 = *(_QWORD **)(qword_141B5FE10 + 128);
    if ( (__int64)(v8[1] - *v8) >> 3 > (unsigned __int64)(unsigned int)v25 )
      *a1 = *(_QWORD *)(*v8 + 8LL * (unsigned int)v25);
  }
LABEL_12:
  nullsub_1(a1);
  return (unsigned int)v2;
}
