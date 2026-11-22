__int64 __fastcall sub_140F49070(__int64 a1, unsigned int a2, unsigned int a3, int a4, int a5, int a6, _BYTE *a7)
{
  unsigned __int64 v11; // rdi
  __int64 v12; // rax
  __int64 v13; // rax
  __int64 v14; // rsi
  __int64 v15; // rcx
  _QWORD *v16; // rax
  _QWORD *v17; // rdx
  char v18; // al
  __int64 v19; // rax
  int v20; // edi
  int v21; // r13d
  __int64 v22; // rax
  int v23; // r14d
  __int64 v24; // rbx
  __int64 v25; // rbx
  int v26; // edi
  int v27; // r14d
  __int64 v28; // rax
  int v29; // ebp
  __int64 v30; // r13
  __int64 v31; // r12
  int v32; // eax
  unsigned int v33; // edi
  __int64 *v34; // rdi
  __int64 *v35; // rbx
  __int64 v37; // rbp
  unsigned __int64 v38; // rax
  unsigned __int64 v39; // r12
  unsigned __int64 v40; // r15
  unsigned __int64 v41; // rdx
  unsigned __int64 v42; // r15
  __int64 v43; // r14
  __int64 *v44; // r13
  __int64 v45; // rbx
  unsigned __int64 v46; // rcx
  __int64 v47; // rbp
  __int64 v48; // rbp
  bool v49; // al
  int v50; // [rsp+28h] [rbp-50h] BYREF
  int v51; // [rsp+2Ch] [rbp-4Ch]
  int v52; // [rsp+30h] [rbp-48h]

  if ( a7 != nullptr )
    *a7 = 0;
  LODWORD(v11) = a5;
  if ( a4 >= 0 )
  {
    v12 = ((__int64 (__fastcall *)(__int64, _QWORD))unk_140F216C0)(a1, a2);
    if ( v12 != 0 )
    {
      v50 = a4;
      v51 = a5;
      v13 = (*(__int64 (__fastcall **)(__int64, int *))(*(_QWORD *)v12 + 32LL))(v12, &v50);
      if ( v13 != 0 )
      {
        v14 = v13;
        if ( a2 != 1 || (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v13 + 48LL))(v13) != 17 )
        {
          if ( a7 == nullptr )
            return v14;
          goto LABEL_21;
        }
        v15 = qword_141B60C30;
        v16 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v15 != 1314013776 )
          {
            v15 += 16;
            if ( v15 == qword_141B60C38 )
              goto LABEL_17;
          }
          if ( v15 == qword_141B60C38 )
            v16 = nullptr;
          else
            v16 = *(_QWORD **)(v15 + 8);
        }
LABEL_17:
        v17 = &unk_141B5A4A0;
        if ( v16 != nullptr )
          v17 = v16;
        v18 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v17 + 48LL))(*v17);
        if ( a7 != nullptr && v18 == 0 )
        {
LABEL_21:
          *a7 = 1;
          return v14;
        }
        if ( v18 == 0 )
          return v14;
      }
    }
  }
  v19 = sub_140F49530(a2, a3);
  if ( v19 == 0 )
    return 0;
  v14 = v19;
  if ( a5 == 0 )
  {
    v32 = dword_141B60C18;
    do
    {
      if ( v32 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 4LL) )
      {
        ((void (__fastcall *)(int *))unk_141750E08)(&dword_141B60C18);
        v32 = dword_141B60C18;
        if ( dword_141B60C18 == -1 )
        {
          sub_1407EB6F0(&unk_141B60C00);
          ((void (__fastcall *)(int *))unk_141750EA0)(&dword_141B60C18);
          v32 = dword_141B60C18;
        }
      }
      v33 = __ROR4__(
              ((unsigned __int64)qword_141B60C08 >> 27) ^ ((unsigned __int64)qword_141B60C08 >> 45),
              (unsigned __int64)qword_141B60C08 >> 59);
      qword_141B60C08 = qword_141B60C10 + 0x5851F42D4C957F2DLL * qword_141B60C08;
      v11 = (1000000000 * (unsigned __int64)v33) >> 32;
    }
    while ( v11 == 0 );
  }
  *(_DWORD *)(v14 + 16) = v11;
  if ( a4 >= 0 )
  {
    *(_DWORD *)(v14 + 12) = a4;
    if ( (int)sub_140F4A860(a1, a2, v14, (unsigned int)a6) >= 0 )
    {
      v20 = *(_DWORD *)(v14 + 12);
      if ( v20 != a4 )
      {
        v21 = *(_DWORD *)(v14 + 16);
        if ( v21 == 0 )
          v21 = *(_DWORD *)(v14 + 12);
        v22 = ((__int64 (__fastcall *)(__int64, _QWORD))unk_140F216C0)(a1, a2);
        v23 = a4 | v20;
        if ( v22 != 0 && v23 >= 0 )
        {
          v24 = v22;
          v51 = v20;
          v50 = a4;
          v52 = v21;
          ((void (__fastcall *)(__int64, int *))unk_1408E73B0)(v22 + 8, &v50);
          *(_BYTE *)(v24 + 88) = 0;
        }
        if ( a2 == 9 || a2 == 3 )
        {
          v25 = *(_QWORD *)(a1 + 152);
          if ( v25 != 0 && v23 >= 0 )
          {
            v51 = v20;
            v50 = a4;
            v52 = v21;
            ((void (__fastcall *)(__int64, int *))unk_1408E73B0)(v25 + 8, &v50);
            *(_BYTE *)(v25 + 88) = 0;
          }
        }
      }
      if ( a6 >= 0 && a6 != a4 )
      {
        v26 = *(_DWORD *)(v14 + 12);
        if ( v26 != a6 )
        {
          v27 = *(_DWORD *)(v14 + 16);
          if ( v27 == 0 )
            v27 = *(_DWORD *)(v14 + 12);
          v28 = ((__int64 (__fastcall *)(__int64, _QWORD))unk_140F216C0)(a1, a2);
          v29 = a6 | v26;
          if ( v28 != 0 && v29 >= 0 )
          {
            v30 = v28;
            v51 = v26;
            v50 = a6;
            v52 = v27;
            ((void (__fastcall *)(__int64, int *))unk_1408E73B0)(v28 + 8, &v50);
            *(_BYTE *)(v30 + 88) = 0;
          }
          if ( a2 == 9 || a2 == 3 )
          {
            v31 = *(_QWORD *)(a1 + 152);
            if ( v31 != 0 && v29 >= 0 )
            {
              v51 = v26;
              v50 = a6;
              v52 = v27;
              ((void (__fastcall *)(__int64, int *))unk_1408E73B0)(v31 + 8, &v50);
              *(_BYTE *)(v31 + 88) = 0;
            }
          }
        }
      }
      goto LABEL_58;
    }
    return 0;
  }
  if ( (int)sub_140F4A860(a1, a2, v14, (unsigned int)a6) < 0 )
    return 0;
LABEL_58:
  v34 = *(__int64 **)(a1 + 1968);
  if ( v34 != nullptr )
  {
    v35 = (__int64 *)v34[1];
    if ( v35 == (__int64 *)v34[2] )
    {
      v37 = (__int64)v35 - *v34;
      v38 = v37 >> 3;
      v39 = (v37 >> 3) + 1;
      v40 = (unsigned __int64)(v37 >> 3) >> 1;
      v41 = 0x1FFFFFFFFFFFFFFFLL - v40;
      v42 = (v37 >> 3) + v40;
      if ( v42 <= v39 )
        v42 = v38 + 1;
      if ( v38 > v41 )
        v42 = 0x1FFFFFFFFFFFFFFFLL;
      v43 = ((__int64 (__fastcall *)(__int64, unsigned __int64))unk_1407E4490)(qword_141ABD470, 8 * v42);
      *(_QWORD *)(v43 + v37) = v14;
      v44 = (__int64 *)v34[1];
      ((void (__fastcall *)(__int64, __int64, char *))unk_141758A00)(v43, *v34, (char *)v35 - *v34);
      if ( v44 != v35 )
        ((void (__fastcall *)(__int64, __int64 *, __int64))unk_141758A00)(v43 + v37 + 8, v35, v34[1] - (_QWORD)v35);
      v45 = *v34;
      if ( *v34 != 0 )
      {
        v46 = v34[2] - v45;
        if ( v46 == -1 )
          v46 = *(unsigned int *)(v45 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v47 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v47) >> 3 > v46)
          && (v48 = *(_QWORD *)(v47 + 8 * v46)) != 0 )
        {
          MEMORY[0x1419475D8](v48 + 32, v45 - *(unsigned int *)(v48 + 120));
          v49 = *(_BYTE *)(v48 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v48 + 64)) != 0;
          if ( !v49 && *(_BYTE *)(v48 + 97) != 0 )
            sub_1412D33C0(v48);
        }
        else
        {
          MEMORY[0x141948990](v45 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *v34 = v43;
      v34[1] = v43 + 8 * v39;
      v34[2] = v43 + 8 * v42;
    }
    else
    {
      *v35 = v14;
      v34[1] += 8;
    }
  }
  return v14;
}
