// THUNK ALIAS -> sub_143BFBA90 (jmp:0x140e46160->0x143bfba90)
char __fastcall sub_143BFBA90(__int64 *a1, int a2, _QWORD *a3)
{
  __int64 v4; // rcx
  __int64 v6; // [rsp+28h] [rbp-10h] BYREF

  switch ( a2 )
  {
    case 1954115685:
      *((_WORD *)a1 + 4) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      return 1;
    case 1853189474:
      *((_BYTE *)a1 + 10) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      return 1;
    case 1851878757:
      (*(void (__fastcall **)(_QWORD, __int64 *))(*(_QWORD *)*a3 + 128LL))(*a3, &v6);
      v4 = *a1;
      if ( *a1 == v6 )
      {
        if ( v4 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v4 - 4)) == 0 )
          sub_1412EC9A0(v4 - 4);
      }
      else
      {
        if ( v4 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v4 - 4)) == 0 )
          sub_1412EC9A0(v4 - 4);
        *a1 = v6;
      }
      return 1;
    default:
      break;
  }
  return 0;
}
