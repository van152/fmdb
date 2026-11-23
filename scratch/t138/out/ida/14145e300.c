__int64 __fastcall sub_14145E300(_QWORD *a1, _QWORD *a2)
{
  unsigned __int64 v2; // r12
  _QWORD *v3; // r13
  __int64 v5; // rsi
  _QWORD *v6; // r14
  _QWORD *v7; // rsi
  bool v8; // zf
  _QWORD *v9; // rbx
  _QWORD *v10; // rdi
  _QWORD *v11; // rbx
  __int64 v12; // rdi
  __int64 v13; // rsi
  __int64 v14; // rdx
  __int64 v15; // r8
  int v17; // eax
  __int64 v18; // r15
  __int64 v19; // r14
  unsigned __int64 v20; // rcx
  __int64 v21; // rdi
  __int64 v22; // rcx
  __int64 v23; // rcx
  __int64 v24; // rsi
  char *v25; // rax
  char *v26; // rbx
  _QWORD *v27; // rsi
  int v28; // ebx
  __int64 v29; // r15
  __int64 v30; // rax
  __int64 v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rsi
  int v34; // edi
  _QWORD *v35; // rsi
  __int64 v36; // r8
  __int64 *v37; // rax
  unsigned __int64 v38; // r14
  unsigned __int64 v39; // rsi
  unsigned __int64 v40; // rbx
  __int64 v41; // rcx
  __int64 v42; // rcx
  __int64 v43; // rdi
  char *v44; // rax
  char *v45; // r13
  _QWORD *v46; // rdi
  __int64 v47; // r15
  __int64 v48; // [rsp+50h] [rbp-30h]
  _QWORD *v49; // [rsp+58h] [rbp-28h]
  int v50; // [rsp+64h] [rbp-1Ch]
  int v51; // [rsp+68h] [rbp-18h] BYREF
  _QWORD *v52; // [rsp+70h] [rbp-10h]
  char v53; // [rsp+7Ah] [rbp-6h] BYREF
  char v54; // [rsp+7Bh] [rbp-5h] BYREF
  int v55; // [rsp+7Ch] [rbp-4h] BYREF
  __int64 v56; // [rsp+80h] [rbp+0h]

  v56 = -2;
  v3 = a2;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v54, a3: 1);
  if ( *(_DWORD *)(v5 + 16) == 0 )
  {
    v6 = (_QWORD *)*a1;
    v7 = (_QWORD *)a1[1];
    v8 = *a1 == (_QWORD)v7;
    v52 = a1;
    if ( !v8 )
    {
      v9 = v6;
      do
      {
        v10 = (_QWORD *)*v9;
        if ( *v9 != 0 )
        {
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v10 + 16LL))(a1: *v10, a2: *v9);
          sub_140E40B80(a1: v10);
        }
        ++v9;
      }
      while ( v9 != v7 );
      v11 = v52;
      v12 = v52[1] - (_QWORD)v7;
      sub_141758A00(a1: v6, a2: v7, a3: v12);
      v52[1] = (char *)v6 + v12;
      a1 = v11;
    }
    v13 = *v3;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v3 + 40LL))(a1: *v3, a2: &v55, a3: 4);
    if ( *(_DWORD *)(v13 + 16) == 0 )
    {
      v17 = v55;
      v18 = v55;
      v19 = *a1;
      v20 = (__int64)(a1[2] - *a1) >> 3;
      if ( v20 < v55 )
      {
        if ( v55 < 0 )
          sub_1400526C0(a1: v20, a2: v14, a3: v15);
        v21 = a1[1];
        v2 = 8LL * v55;
        if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
          && (v22 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v22) >> 3 > v2)
          && (v23 = *(_QWORD *)(v22 + ((__int64)v55 << 6))) != 0 )
        {
          v24 = *(unsigned int *)(v23 + 88);
          v25 = (char *)sub_1407E58C0(a1: v23, a2: *(unsigned int *)(v23 + 80));
        }
        else
        {
          v24 = *(unsigned int *)(qword_141ABE200 + 48);
          v25 = (char *)sub_141601260(a1: (unsigned int)(v24 + v2), a2: 4096, a3: v15);
        }
        v26 = v25;
        if ( v24 != 0 )
        {
          *(_DWORD *)v25 = v2;
          v26 = &v25[v24];
        }
        v27 = v52;
        sub_141758A00(a1: v26, a2: *v52, a3: v52[1] - *v52);
        if ( *v52 != 0 )
          sub_1407E6420(a1: qword_141ABE200, a2: *v52, a3: v52[2] - *v52);
        *v52 = v26;
        v27[1] = &v26[v21 - v19];
        v27[2] = &v26[8 * v18];
        v17 = v55;
      }
      if ( v17 <= 0 )
      {
        LOBYTE(v2) = 1;
        return (unsigned int)v2;
      }
      v28 = 0;
      v49 = v3;
      while ( 1 )
      {
        if ( dword_141B5D820 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B5D820);
          if ( dword_141B5D820 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B5D7D0,
              a2: 1100140307,
              a3: 1024,
              a4: 24,
              a5: 0,
              a6: 0,
              a7: 1024,
              a8: 4096);
            sub_141751048(a1: sub_140E40CF0);
            sub_141750EA0(a1: &dword_141B5D820);
          }
        }
        v29 = sub_1407E58C0(a1: &unk_141B5D7D0, a2: 24);
        *(_QWORD *)v29 = 0;
        *(_QWORD *)(v29 + 8) = 0;
        *(_QWORD *)(v29 + 16) = 0;
        v30 = sub_14083D4F0();
        *(_QWORD *)(v29 + 8) = 0;
        *(_QWORD *)v29 = v30 + 8;
        *(_DWORD *)(v29 + 16) = 124518401;
        *(_BYTE *)(v29 + 20) = 0;
        v31 = *v3;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v3 + 40LL))(a1: *v3, a2: &v53, a3: 1);
        if ( *(_DWORD *)(v31 + 16) != 0 )
          break;
        v32 = *v3;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v3 + 40LL))(a1: *v3, a2: v29 + 20, a3: 1);
        if ( *(_DWORD *)(v32 + 16) != 0 )
          break;
        v33 = *v3;
        if ( *v3 != 0 )
        {
          _InterlockedIncrement((volatile signed __int32 *)(v33 + 8));
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v33 + 40LL))(a1: v33, a2: v29 + 16, a3: 4);
        }
        v34 = *(_DWORD *)(v33 + 16);
        if ( _InterlockedDecrement((volatile signed __int32 *)(v33 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v33)(a1: v33, a2: 1);
        v35 = v52;
        if ( v34 != 0 )
          break;
        sub_1408386A0(a1: *v3, a2: &v51, a3: v29);
        LOBYTE(v2) = v51 == 0;
        if ( v51 == 0 )
        {
          v37 = (__int64 *)v35[1];
          if ( v37 == (__int64 *)v35[2] )
          {
            v50 = v28;
            v48 = v35[1];
            v38 = ((__int64)v37 - *v35) >> 3;
            v39 = v38 + (v38 >> 1);
            if ( v39 <= v38 + 1 )
              v39 = v38 + 1;
            if ( v38 > 0x1FFFFFFFFFFFFFFFLL - (v38 >> 1) )
              v39 = 0x1FFFFFFFFFFFFFFFLL;
            v40 = 8 * v39;
            if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
              && (v41 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v41) >> 3 > v40)
              && (v42 = *(_QWORD *)(v41 + (v39 << 6))) != 0 )
            {
              v43 = *(unsigned int *)(v42 + 88);
              v44 = (char *)sub_1407E58C0(a1: v42, a2: *(unsigned int *)(v42 + 80));
            }
            else
            {
              v43 = *(unsigned int *)(qword_141ABE200 + 48);
              v44 = (char *)sub_141601260(a1: (unsigned int)(v43 + v40), a2: 4096, a3: v36);
            }
            v45 = v44;
            if ( v43 != 0 )
            {
              *(_DWORD *)v44 = v40;
              v45 = &v44[v43];
            }
            *(_QWORD *)&v45[8 * v38] = v29;
            v46 = v52;
            v47 = v52[1];
            sub_141758A00(a1: v45, a2: *v52, a3: v48 - *v52);
            if ( v47 != v48 )
              sub_141758A00(a1: &v45[8 * v38 + 8], a2: v48, a3: v46[1] - v48);
            if ( *v46 != 0 )
              sub_1407E6420(a1: qword_141ABE200, a2: *v46, a3: v46[2] - *v46);
            *v46 = v45;
            v46[1] = &v45[8 * v38 + 8];
            v46[2] = &v45[8 * v39];
            v3 = v49;
            v28 = v50;
          }
          else
          {
            *v37 = v29;
            v35[1] += 8LL;
          }
          if ( ++v28 < v55 )
            continue;
        }
        return (unsigned int)v2;
      }
    }
  }
  LODWORD(v2) = 0;
  return (unsigned int)v2;
}
