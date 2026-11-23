void __fastcall sub_140EDAE60(__int64 a1, int a2, __int64 a3)
{
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax

  switch ( a2 )
  {
    case 1131443302:
      v6 = sub_140FE35F0();
      if ( v6 != 0 )
        (*(void (__fastcall **)(__int64, __int64, __int64, _QWORD))(*(_QWORD *)qword_141B5EF38 + 208LL))(
          qword_141B5EF38,
          v6,
          a3,
          *(unsigned int *)(a1 + 12));
      break;
    case 1131373414:
      v7 = sub_140FE35F0();
      if ( v7 != 0 )
        (*(void (__fastcall **)(__int64, __int64, __int64, _QWORD))(*(_QWORD *)qword_141B5EF38 + 176LL))(
          qword_141B5EF38,
          v7,
          a3,
          *(unsigned int *)(a1 + 12));
      break;
    case 1130587756:
      v5 = sub_140FE35F0();
      if ( v5 != 0 )
        (*(void (__fastcall **)(__int64, __int64, __int64, _QWORD))(*(_QWORD *)qword_141B5EF38 + 160LL))(
          qword_141B5EF38,
          v5,
          a3,
          *(unsigned int *)(a1 + 12));
      break;
    default:
      break;
  }
}
