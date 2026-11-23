__int64 __fastcall sub_143B934A0(__int64 a1, __int64 *a2, char a3)
{
  _QWORD *v6; // rsi
  __int64 v7; // r8
  __int64 v8; // r8
  _QWORD *v9; // rsi
  __int64 v10; // r8
  __int64 v11; // r8
  _QWORD *v12; // rsi
  __int64 v13; // rcx
  _QWORD *v14; // rbx
  __int64 v15; // rsi
  _QWORD *v16; // rdi
  __int64 v17; // rax
  _DWORD *v18; // rcx
  __int64 v19; // rdx
  int v20; // eax
  __int64 result; // rax
  int *v22; // rcx
  char v23; // [rsp+4Bh] [rbp-2Dh] BYREF
  int v24; // [rsp+4Ch] [rbp-2Ch] BYREF
  char v25; // [rsp+50h] [rbp-28h] BYREF

  v6 = *(_QWORD **)a1;
  v7 = *(_QWORD *)(*(_QWORD *)a1 + 16LL);
  if ( *(int **)(*(_QWORD *)a1 + 24LL) == &v24 )
  {
    v8 = v7 + 4;
  }
  else
  {
    if ( v7 != 0 && *v6 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v6 + 40LL))(a1: *v6, a2: v6[1]);
    v6[1] = &v24;
    v8 = 4;
  }
  v6[2] = v8;
  v6[3] = &v25;
  v23 = 0;
  v9 = *(_QWORD **)a1;
  v10 = *(_QWORD *)(*(_QWORD *)a1 + 16LL);
  if ( *(char **)(*(_QWORD *)a1 + 24LL) == &v23 )
  {
    v11 = v10 + 1;
  }
  else
  {
    if ( v10 != 0 && *v9 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v9 + 40LL))(a1: *v9, a2: v9[1]);
    v9[3] = 0;
    v9[1] = &v23;
    v11 = 1;
  }
  v9[2] = v11;
  v9[3] = &v24;
  v12 = *(_QWORD **)a1;
  if ( *(_QWORD *)(*(_QWORD *)a1 + 16LL) != 0 && *v12 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v12 + 40LL))(a1: *v12, a2: v12[1]);
  v12[3] = 0;
  v12[2] = 0;
  v12[1] = 0;
  if ( v23 == 0 )
  {
    result = v24;
LABEL_32:
    *a2 = result;
    return result;
  }
  v13 = 216;
  if ( a3 != 2 )
    v13 = 8LL * (a3 == 1) + 200;
  v14 = *(_QWORD **)((char *)&qword_141B5FDA8 + v13);
  if ( dword_141B5D0D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5D0D0);
    if ( dword_141B5D0D0 == -1 )
    {
      sub_1407E53D0(
        a1: (unsigned int)&unk_141B5D080,
        a2: 1100152899,
        a3: 10000,
        a4: 24,
        a5: 0,
        a6: 0,
        a7: 10000,
        a8: 4096);
      sub_141751048(a1: sub_140E05230);
      sub_141750EA0(a1: &dword_141B5D0D0);
    }
  }
  v15 = sub_1407E58C0(a1: &unk_141B5D080, a2: 24);
  *(_QWORD *)v15 = 0;
  *(_DWORD *)(v15 + 8) = -1;
  *(_QWORD *)(v15 + 12) = 0xFF00FFFF0000FFFFuLL;
  v16 = *(_QWORD **)a1;
  if ( v16[2] != 0 && *v16 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v16 + 40LL))(a1: *v16, a2: v16[1]);
  v16[3] = 0;
  v16[2] = 0;
  v16[1] = 0;
  sub_1410B9440(a1: v15, a2: v16);
  v17 = v24;
  if ( v24 >= (int)((v14[1] - *v14) >> 3) )
  {
LABEL_31:
    sub_1410B9CE0(a1: v14, a2: v15);
    result = *(int *)(v15 + 8);
    goto LABEL_32;
  }
  v18 = **(_DWORD ***)(*v14 + 8LL * v24);
  if ( v18 != nullptr && *v18 != 0 )
  {
    LODWORD(v19) = 1100232177;
    if ( *(_QWORD *)v15 != 0 )
    {
      v19 = *(_QWORD *)v15 + 4LL;
      v20 = **(_DWORD **)v15;
    }
    else
    {
      v20 = 0;
    }
    if ( (unsigned int)sub_140811EA0(a1: (int)v18 + 4, a2: v19, a3: -1, a4: *v18, a5: v20) != 0 )
      goto LABEL_31;
    v17 = v24;
  }
  *a2 = v17;
  v22 = *(int **)v15;
  if ( *(_QWORD *)v15 != 0 && _InterlockedDecrement(v22 - 1) == 0 )
    sub_1412EC9A0(a1: v22 - 1);
  return sub_140E050C0(a1: v15);
}
