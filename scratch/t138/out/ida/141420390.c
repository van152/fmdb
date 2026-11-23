__int64 __fastcall sub_141420390(__int64 a1, __int64 *a2)
{
  __int64 v3; // rax
  char *v4; // r14
  __int64 v5; // r8
  char *v6; // rsi
  __int64 v7; // rax
  __int64 v8; // rsi
  __int64 v9; // r8
  bool v10; // zf
  char *v11; // rdi
  __int64 v12; // r8
  _QWORD *v13; // rbx
  _BYTE *v14; // rax
  __int64 v15; // rdi
  unsigned __int64 v16; // rcx
  __int64 v17; // rbx
  __int64 v18; // rbx
  bool v19; // al
  __int64 v20; // rbx
  bool v21; // al
  __int64 v22; // r15
  void (__fastcall ***v23)(_QWORD, __int64); // rcx
  _DWORD *v25; // [rsp+28h] [rbp-28h] BYREF
  char *v26; // [rsp+30h] [rbp-20h]
  __int64 v27; // [rsp+38h] [rbp-18h]
  __int64 *v28; // [rsp+40h] [rbp-10h]
  char v29; // [rsp+4Eh] [rbp-2h] BYREF
  char v30; // [rsp+4Fh] [rbp-1h] BYREF
  __int64 v31; // [rsp+50h] [rbp+0h] BYREF

  v31 = -2;
  v3 = *a2;
  v25 = (_DWORD *)v3;
  if ( v3 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v3 + 8));
  v26 = &v29;
  v27 = 1;
  v28 = (__int64 *)&v30;
  if ( v25 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: &v29, a3: 1);
  v26 = (char *)(a1 + 198);
  v27 = 2;
  v28 = (__int64 *)(a1 + 200);
  if ( v25 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: a1 + 198, a3: 2);
    v26 = (char *)(a1 + 176);
    v27 = 8;
    v4 = (char *)(a1 + 184);
    v28 = (__int64 *)(a1 + 184);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: a1 + 176, a3: 8);
  }
  else
  {
    v4 = (char *)(a1 + 184);
  }
  v26 = (char *)(a1 + 152);
  v27 = 8;
  v28 = (__int64 *)(a1 + 160);
  if ( v29 != 5 )
  {
    v7 = sub_140EE7C20();
    *(_QWORD *)(a1 + 160) = v7;
    if ( v7 != 0 )
    {
      v8 = v7;
      if ( v27 != 0 && v25 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26);
      v28 = nullptr;
      v27 = 0;
      v26 = nullptr;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, _DWORD **))(*(_QWORD *)v8 + 32LL))(a1: v8, a2: &v25) == 0 )
        goto LABEL_73;
    }
    v6 = (char *)(a1 + 192);
    if ( v28 == (__int64 *)(a1 + 192) )
    {
      v10 = v27 == -6;
      v9 = v27 + 6;
      v27 += 6;
      v28 = (__int64 *)(a1 + 198);
      if ( v10 )
        goto LABEL_24;
    }
    else
    {
      if ( v27 != 0 && v25 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26, a3: v27);
      v26 = (char *)(a1 + 192);
      v27 = 6;
      v28 = (__int64 *)(a1 + 198);
      v9 = 6;
    }
    if ( v25 != nullptr )
    {
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26, a3: v9);
LABEL_24:
      v26 = (char *)(a1 + 200);
      v27 = 1;
      v28 = (__int64 *)(a1 + 201);
      if ( v25 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: a1 + 200, a3: 1);
    }
    v26 = v4;
    v27 = 8;
    v28 = (__int64 *)(a1 + 192);
    v30 = 0;
    v11 = &v30;
    if ( v6 == &v30 )
    {
      v12 = 9;
      v11 = v4;
    }
    else
    {
      if ( v25 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v4, a3: 8);
      v26 = &v30;
      v12 = 1;
    }
    v27 = v12;
    v28 = &v31;
    if ( v25 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v11);
    v28 = nullptr;
    v27 = 0;
    v26 = nullptr;
    if ( v30 != 0 )
    {
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(a1: &unk_141B59A68);
          sub_141751048(a1: sub_1407E4B20);
          sub_141750EA0(a1: &dword_141B59AA8);
        }
      }
      v13 = (_QWORD *)sub_1407E4490(a1: &unk_141B59A68, a2: 32);
      *v13 = 0;
      v13[1] = 0;
      v13[2] = 0;
      v13[3] = 0;
      v14 = (_BYTE *)qword_141ABD470;
      if ( qword_141ABD470 == 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(a1: &unk_141B59A68);
            sub_141751048(a1: sub_1407E4B20);
            sub_141750EA0(a1: &dword_141B59AA8);
          }
        }
        qword_141ABD470 = (__int64)&unk_141B59A68;
        v14 = &unk_141B59A68;
      }
      v13[3] = 0;
      v13[2] = 0;
      v13[1] = 0;
      *v13 = 0;
      v15 = *(_QWORD *)(a1 + 168);
      *(_QWORD *)(a1 + 168) = v13;
      if ( v15 != 0 )
      {
        v6 = *(char **)v15;
        if ( *(_QWORD *)v15 != 0 )
        {
          v16 = *(_QWORD *)(v15 + 16) - (_QWORD)v6;
          if ( v16 == -1 )
            v16 = *(unsigned int *)&v6[-*((unsigned int *)v14 + 12)];
          if ( v14[52] != 0
            && (v17 = *((_QWORD *)v14 + 3), (*((_QWORD *)v14 + 4) - v17) >> 3 > v16)
            && (v18 = *(_QWORD *)(v17 + 8 * v16)) != 0 )
          {
            v6 -= *(unsigned int *)(v18 + 120);
            MEMORY[0x1419475D8](a1: v18 + 32, a2: v6);
            v19 = *(_BYTE *)(v18 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 64)) != 0;
            if ( !v19 && *(_BYTE *)(v18 + 97) != 0 )
              sub_1412D33C0(a1: v18);
          }
          else
          {
            v6 -= *((unsigned int *)v14 + 12);
            MEMORY[0x141948990](a1: v6);
          }
          *(_QWORD *)(v15 + 16) = 0;
          *(_QWORD *)(v15 + 8) = 0;
          *(_QWORD *)v15 = 0;
        }
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(a1: &unk_141B59A68);
            sub_141751048(a1: sub_1407E4B20);
            sub_141750EA0(a1: &dword_141B59AA8);
          }
        }
        if ( byte_141B59A9C != 0
          && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0x101
          && (v20 = *(_QWORD *)(qword_141B59A80 + 256)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v20 + 32, a2: v15 - *(unsigned int *)(v20 + 120));
          v21 = *(_BYTE *)(v20 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 64)) != 0;
          if ( !v21 && *(_BYTE *)(v20 + 97) != 0 )
            sub_1412D33C0(a1: v20);
        }
        else
        {
          MEMORY[0x141948990](a1: v15 - (unsigned int)dword_141B59A98);
        }
        v13 = *(_QWORD **)(a1 + 168);
      }
      if ( v27 != 0 && v25 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26);
      v28 = nullptr;
      v27 = 0;
      v26 = nullptr;
      if ( (unsigned __int8)sub_141727790(a1: v13, a2: &v25) == 0 )
        goto LABEL_73;
      if ( v27 != 0 && v25 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26);
    }
    v28 = nullptr;
    v27 = 0;
    v26 = nullptr;
    if ( (unsigned __int8)sub_141727C60(a1: a1 + 8, a2: &v25) != 0 )
    {
      v22 = a1 + 80;
      if ( v27 != 0 && v25 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26);
      v28 = nullptr;
      v27 = 0;
      v26 = nullptr;
      if ( (unsigned __int8)sub_141727C60(a1: v22, a2: &v25) != 0 )
      {
        if ( v27 != 0 && v25 != nullptr )
          (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26);
        v28 = nullptr;
        v27 = 0;
        v26 = nullptr;
        LOBYTE(v6) = v25[4] == 0;
LABEL_74:
        v5 = v27;
        if ( v27 == 0 )
          goto LABEL_77;
        goto LABEL_75;
      }
    }
LABEL_73:
    LODWORD(v6) = 0;
    goto LABEL_74;
  }
  v5 = 8;
  LODWORD(v6) = 0;
LABEL_75:
  if ( v25 == nullptr )
    return (unsigned int)v6;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: v26, a3: v5);
LABEL_77:
  v23 = (void (__fastcall ***)(_QWORD, __int64))v25;
  v28 = nullptr;
  v27 = 0;
  v26 = nullptr;
  if ( v25 != nullptr && _InterlockedDecrement(v25 + 2) == 0 )
    (**v23)(a1: v23, a2: 1);
  return (unsigned int)v6;
}
