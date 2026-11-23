// THUNK ALIAS -> sub_143B540C0 (jmp:0x140dbca60->0x143b540c0)
__int64 __fastcall sub_143B540C0(__int64 a1, __int64 a2, _QWORD *a3)
{
  unsigned int v5; // eax
  __int64 v7[4]; // [rsp+28h] [rbp-20h] BYREF

  if ( *a3 == a1 )
  {
    v5 = *((_DWORD *)a3 + 2);
    *(_WORD *)(a2 + 2) = v5 >> 17;
    *(_WORD *)a2 = (v5 >> 8) & 0x1FF | ((_WORD)v5 << 9);
  }
  else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
  {
    (*(void (__fastcall **)(_QWORD, __int64 *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v7, a3);
    sub_1413CA830((_DWORD *)a2, v7);
  }
  else
  {
    *(_DWORD *)a2 = 124518401;
  }
  return a2;
}
