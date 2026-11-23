bool __fastcall sub_143C89D90(__int64 *a1, _QWORD *a2, char a3)
{
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rbx
  int v8; // ebp
  int v10; // [rsp+20h] [rbp-28h] BYREF
  _DWORD v11[9]; // [rsp+24h] [rbp-24h] BYREF

  if ( a3 != 0 )
  {
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v10, a3: 4);
    if ( v10 == -1 )
      v5 = 0;
    else
      v5 = sub_140F74650(a1: qword_141B5FE38);
    *a1 = v5;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v10, a3: 4);
    if ( v10 == -1 )
      v6 = 0;
    else
      v6 = sub_140F74650(a1: qword_141B5FE38);
  }
  else
  {
    (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11, a3: 4);
    *a1 = v11[0];
    (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11, a3: 4);
    v6 = v11[0];
  }
  a1[1] = v6;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 20, a3: 1);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 21, a3: 1);
  v7 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v7 + 8));
    (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1 + 2, a3: 4);
  }
  v8 = *(_DWORD *)(v7 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v7 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v7)(a1: v7, a2: 1);
  if ( v8 != 0 )
    return false;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 22, a3: 1);
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
